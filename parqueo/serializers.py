from rest_framework.serializers import ModelSerializer
from parqueo.models import Parking, Address, OpeningHours, Price, VehicleEntry, Details

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id','name', 'capacity', 'phone', 'email', 'user', 'spaces_available', 'url_image', 'description']
        extra_kwargs = {
            'phone': {'required': False},
            'email': {'required': False},
            'user': {'required': False},
            'spaces_available': {'required': False},
            'url_image': {'required': False},
            'description': {'required': False},
        }

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','city', 'street', 'longitude', 'latitude', 'parking']
        extra_kwargs = {
            'city': {'required': False},
            'street': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'parking': {'required': False},
        }

class OpeningHoursSerializer(ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ['id','day', 'open_time', 'close_time', 'parking']
        extra_kwargs = {
            'day': {'required': False},
            'open_time': {'required': False},
            'close_time': {'required': False},
            'parking': {'required': False},
        }

class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = ['id','type_vehicle', 'price_per_hour', 'parking']
        extra_kwargs = {
            'type_vehicle': {'required': False},
            'price_per_hour': {'required': False},
            'parking': {'required': False},
        }

class VehicleEntrySerializer(ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = ['id','vehicle', 'user', 'parking','is_reserva','details']
        extra_kwargs = {
            'vehicle': {'required': False},
            'user': {'required': False},
            'parking': {'required': False},
            'is_reserva': {'required': False},
            'details': {'required': False},
        }

class DetailsSerializer(ModelSerializer):
    class Meta:
        model = Details
        fields = ['id', 'starttime', 'endtime', 'totalamount','price', 'extratime']
        extra_kwargs = {
            'starttime': {'required': False},
            'endtime': {'required': False},
            'totalamount': {'required': False},
            'price': {'required': False},
            'extratime': {'required': False},
        }
