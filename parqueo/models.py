from django.db import models
from accounts.models import User
from extratime.models import ExtraTime
from vehiculos.models import TypeVehicle, Vehicle

class Parking(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parking')
    spaces_available = models.IntegerField()
    url_image = models.CharField(max_length=200)
    description = models.CharField(max_length=150)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'parking'
        ordering = ['-created_at']

class Address(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
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
    price = models.FloatField()
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='prices')
    is_reservation = models.BooleanField(default=False)
    is_entry_fee = models.BooleanField(default=True)
    is_pricehour = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'price'
        ordering = ['-created_at']

class PriceHour(models.Model):
    start_time = models.TimeField(default=None, null=True)
    end_time = models.TimeField(default=None,null=True)
    total_time = models.IntegerField()
    price = models.ForeignKey(Price,on_delete=models.CASCADE,related_name="price_hour")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'pricehour'
        ordering = ['-created_at']



class VehicleEntry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='entries',null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='entries',null=True)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='entries')
    is_reserva = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=50, default=False)
    is_userexternal = models.BooleanField(default=False)
    class Meta:
        db_table = 'vehicleentry'
        ordering = ['-created_at']

class Details(models.Model):
    starttime = models.DateTimeField(null=True)
    endtime = models.DateTimeField(null=True)
    totalamount = models.FloatField(null=True)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='prices', null=True, blank=True)
    extratime = models.ForeignKey(ExtraTime, on_delete=models.CASCADE, related_name='extra_time',null=True, blank=True)
    vehicle_entry = models.ForeignKey(VehicleEntry, on_delete=models.CASCADE, related_name='details', null=True, blank=True)
    is_userexternal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'details'
        ordering = ['-created_at']


