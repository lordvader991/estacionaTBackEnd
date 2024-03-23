from django.db import models
from vehiculos.models import Vehicle
from parqueo.models import Price



class ExtraTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'extratime'
        ordering=['-created_at']



class Reservation(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    totalamount = models.FloatField()
    date = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reservations')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservations')
    extratime = models.ForeignKey(ExtraTime, on_delete=models.CASCADE, related_name='reservations')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'reservation'
        ordering = ['-created_at']
