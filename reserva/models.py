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
    def calculate_total_earnings_per_parking():
        return (Reservation.objects
                .values(parking=F('vehicle_entry__parking'))
                .annotate(
                    total_earnings=Sum('total_amount'),
                    vehicle_count=Count('vehicle_entry')
                )
                .order_by('parking'))
