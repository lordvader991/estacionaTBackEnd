from django.db import models
from accounts.models import User
from extratime.models import ExtraTime
from parqueo.models import Price, VehicleEntry, Parking, Details
from django.db.models import Sum, Count, F, Q, DateField
from django.db.models.functions import Cast, TruncDate

class Reservation(models.Model):
    class StateChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        CONFIRMED = 'CONFIRMED', 'Confirmada'
        ACTIVE = 'ACTIVE', 'Activa'
        COMPLETED = 'COMPLETED', 'Completada'
        CANCELLED = 'CANCELLED', 'Cancelada'
        NO_SHOW = 'NO_SHOW', 'No Presentado'
        MODIFIED = 'MODIFIED', 'Modificada'
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.FloatField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservation')
    extra_time = models.ForeignKey(ExtraTime, on_delete=models.SET_NULL, related_name='extratime',null=True,blank=True,default=None)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    reservation_date = models.DateField(default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True,blank=True)
    vehicle_entry = models.ForeignKey(VehicleEntry, on_delete=models.CASCADE, related_name='vehicle_entry', null=True, blank=True)
    state = models.CharField(max_length=10, choices=StateChoices.choices, default=StateChoices.PENDING)


    class Meta:
        db_table = 'reservationdetails'
        ordering = ['-created_at']

    @staticmethod
    def calculate_total_earnings_and_vehicle_count_per_parking(parking_id):
        # Earnings from reservations
        earnings = Reservation.objects.filter(vehicle_entry__parking_id=parking_id).values(
            parking_earning_id=F('vehicle_entry__parking'),
            earning_date=F('reservation_date')
        ).annotate(
            total_earnings=Sum('total_amount'),
            reservation_vehicle_count=Count('vehicle_entry')
        ).order_by('parking_earning_id', 'earning_date')

        # Vehicle entries
        vehicle_entries = VehicleEntry.objects.filter(parking_id=parking_id).annotate(
            entry_date=TruncDate('created_at')
        ).values(
            parking_entry_id=F('parking'),
            entry_date=F('entry_date')
        ).annotate(
            entry_vehicle_count=Count('id'),
            external_vehicle_count=Count('id', filter=Q(is_userexternal=True))
        ).order_by('parking_entry_id', 'entry_date')

        # Details entries
        details_entries = Details.objects.filter(vehicle_entry__parking_id=parking_id).annotate(
            details_date=TruncDate('starttime')
        ).values(
            parking_details_id=F('vehicle_entry__parking'),
            details_date=F('details_date')
        ).annotate(
            external_vehicle_count=Count('vehicle_entry', filter=Q(vehicle_entry__is_userexternal=True)),
            details_total_earnings=Sum('totalamount')
        ).order_by('parking_details_id', 'details_date')

        parking_data = {}

        # Process vehicle entries
        for entry in vehicle_entries:
            key = (entry['parking_entry_id'], entry['entry_date'])
            parking_data[key] = {
                'entry_vehicle_count': entry['entry_vehicle_count'],
                'external_vehicle_count': entry['external_vehicle_count'],
                'total_earnings': 0,
                'reservation_vehicle_count': 0,
                'date': entry['entry_date']
            }

        # Process earnings
        for earning in earnings:
            key = (earning['parking_earning_id'], earning['earning_date'])
            if key in parking_data:
                parking_data[key]['total_earnings'] += earning['total_earnings']
                parking_data[key]['reservation_vehicle_count'] += earning['reservation_vehicle_count']
            else:
                parking_data[key] = {
                    'total_earnings': earning['total_earnings'],
                    'reservation_vehicle_count': earning['reservation_vehicle_count'],
                    'entry_vehicle_count': 0,
                    'external_vehicle_count': 0,
                    'date': earning['earning_date']
                }

        # Process details entries
        for detail in details_entries:
            key = (detail['parking_details_id'], detail['details_date'])
            if key in parking_data:
                parking_data[key]['external_vehicle_count'] += detail['external_vehicle_count']
                parking_data[key]['total_earnings'] += detail['details_total_earnings']
            else:
                parking_data[key] = {
                    'total_earnings': detail['details_total_earnings'],
                    'reservation_vehicle_count': 0,
                    'entry_vehicle_count': 0,
                    'external_vehicle_count': detail['external_vehicle_count'],
                    'date': detail['details_date']
                }

        result = []
        for (parking_id, date), data in parking_data.items():
            result.append({
                'parking_id': parking_id,
                'date': data['date'],
                'total_earnings': data.get('total_earnings', 0),
                'reservation_vehicle_count': data.get('reservation_vehicle_count', 0),
                'entry_vehicle_count': data.get('entry_vehicle_count', 0),
                'external_vehicle_count': data.get('external_vehicle_count', 0)
            })

        return result
