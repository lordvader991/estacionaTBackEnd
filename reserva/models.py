from django.db import models
from accounts.models import User
from extratime.models import ExtraTime
from parqueo.models import Price

class Reservation(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.FloatField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservation')
    extra_time = models.ForeignKey(ExtraTime, on_delete=models.SET_NULL, related_name='extratime',null=True,blank=True,default=None)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    reservation_date = models.DateField(default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'reservationdetails'
        ordering = ['-created_at'] 