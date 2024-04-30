from django.db import models
from extratime.models import ExtraTime
from parqueo.models import Price

class Reservation(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.FloatField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservation')
    extra_time = models.ForeignKey(ExtraTime, on_delete=models.SET_NULL, related_name='reservation',null=True,blank=True,default=None)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    reservation_date = models.DateField(default=None)
    class Meta:
        db_table = 'reservationdetails'
        ordering = ['-created_at'] 