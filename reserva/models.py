from django.db import models
from accounts.models import User
from extratime.models import ExtraTime
from parqueo.models import Price, VehicleEntry, Parking
from django.db.models import Sum,F, Count

class Reservation(models.Model):
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

    class Meta:
        db_table = 'reservationdetails'
        ordering = ['-created_at']

    @staticmethod
    def calculate_total_earnings_and_vehicle_count_per_parking():
        from django.db.models import Sum, Count, F, Q

        earnings = Reservation.objects.values(parking_earning=F('vehicle_entry__parking')).annotate(
            total_earnings=Sum('total_amount'),
            reservation_vehicle_count=Count('vehicle_entry')
        ).order_by('parking_earning')

        vehicle_entries = VehicleEntry.objects.values(parking_entry=F('parking')).annotate(
            entry_vehicle_count=Count('id'),
            external_vehicle_count=Count('id', filter=Q(is_userexternal=True))
        ).order_by('parking_entry')

        parking_data = {}
        for entry in vehicle_entries:
            parking_data[entry['parking_entry']] = {
                'entry_vehicle_count': entry['entry_vehicle_count'],
                'external_vehicle_count': entry['external_vehicle_count']
            }

        for earning in earnings:
            if earning['parking_earning'] in parking_data:
                parking_data[earning['parking_earning']]['total_earnings'] = earning['total_earnings']
                parking_data[earning['parking_earning']]['reservation_vehicle_count'] = earning['reservation_vehicle_count']
            else:
                parking_data[earning['parking_earning']] = {
                    'total_earnings': earning['total_earnings'],
                    'reservation_vehicle_count': earning['reservation_vehicle_count'],
                    'entry_vehicle_count': 0,
                    'external_vehicle_count': 0
                }

        result = []
        for parking, data in parking_data.items():
            result.append({
                'parking_id': parking,
                'total_earnings': data.get('total_earnings', 0),
                'reservation_vehicle_count': data.get('reservation_vehicle_count', 0),
                'entry_vehicle_count': data.get('entry_vehicle_count', 0),
                'external_vehicle_count': data.get('external_vehicle_count', 0)
            })

        return result
