from rest_framework.serializers import ModelSerializer
from parqueo.models import  Parking, Address, OpeningHours, Price, VehicleEntry, Details

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id','name', 'capacity', 'phone', 'email', 'user', 'spaces_available', 'url_image', 'description']

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','city', 'street', 'longitude', 'latitude', 'parking']

class OpeningHoursSerializer(ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ['id','day', 'open_time', 'close_time', 'parking']

class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = ['id','type_vehicle', 'price_per_hour', 'parking']

class VehicleEntrySerializer(ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = ['id','vehicle', 'user', 'parking','is_reserva','details']

class DetailsSerializer(ModelSerializer):
    class Meta:
        model = Details
        fields = ['id', 'starttime', 'endtime', 'totalamount','price', 'extratime']
