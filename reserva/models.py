from django.db import models


class ExtraTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'extratime'
        ordering=['-created_at']

""" class ReservationDetails(models.Model):
    starttime = models.IntegerField()
    endtime = models.IntegerField()
    totalamount = models.FloatField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservations')
    extratime = models.ForeignKey(ExtraTime, on_delete=models.CASCADE, related_name='reservations')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'reservationdetails'
        ordering = ['-created_at'] """


