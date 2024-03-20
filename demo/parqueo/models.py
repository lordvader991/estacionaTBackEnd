from django.db import models
from accounts.models import User
from vehiculos.models import TypeVehicle, Vehicle

class Parking(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parking')
    spaces_available = models.IntegerField()
    url_image = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'parking'
        ordering = ['-created_at']



class Address(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='addresses')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'address'
        ordering = ['-created_at']


class OpeningHours(models.Model):
    day = models.CharField(max_length=15)
    open_time = models.TimeField()
    close_time = models.TimeField()
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='opening_hours')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'openinghours'
        ordering = ['-created_at']



class Price(models.Model):
    type_vehicle = models.ForeignKey(TypeVehicle, on_delete=models.CASCADE, related_name='prices')
    price_per_hour = models.FloatField()
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='prices')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'price'
        ordering = ['-created_at']



class VehicleEntry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='entries')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='entries')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'vehicleentry'
        ordering = ['-created_at']
