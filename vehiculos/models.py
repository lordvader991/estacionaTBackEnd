from django.db import models
from accounts.models import User

class TypeVehicle(models.Model):
        name = models.CharField(max_length=15)
        description = models.CharField(max_length=100)
        created_at= models.DateTimeField(auto_now_add=True)
        updated_at= models.DateTimeField(auto_now=True)
        class Meta:
            db_table = 'typevehicle'
            ordering=['-created_at']


class Vehicle(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_plate = models.CharField(max_length=15)
    type_vehicle = models.ForeignKey(TypeVehicle, on_delete=models.CASCADE, related_name='vehicles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    is_ownparking = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'vehicle'
        ordering = ['-created_at']
