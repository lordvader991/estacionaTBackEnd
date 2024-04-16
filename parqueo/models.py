from django.db import models
from accounts.models import User
from vehiculos.models import TypeVehicle, Vehicle
from reserva.models import ExtraTime

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
    price = models.FloatField()
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='prices')
    is_reservation = models.BooleanField(default=False)
    is_pricehour = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'price'
        ordering = ['-created_at']

class PriceHour(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_time = models.IntegerField()
    price = models.ForeignKey(Price,on_delete=models.CASCADE,related_name="price_hour")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'pricehour'
        ordering = ['-created_at']

class Details(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    totalamount = models.FloatField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='reservations')
    extratime = models.ForeignKey(ExtraTime, on_delete=models.CASCADE, related_name='reservations')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'details'
        ordering = ['-created_at']

class VehicleEntry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    parking = models.ForeignKey('Parking', on_delete=models.CASCADE, related_name='entries')
    is_reserva = models.BooleanField(default=False)
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='entries', default=1)  # Aquí especifica el ID predeterminado del detalle existente
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehicleentry'
        ordering = ['-created_at']