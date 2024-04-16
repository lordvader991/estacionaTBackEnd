from rest_framework.serializers import ModelSerializer
from parqueo.models import  Parking, Address, OpeningHours, Price, PriceHour, VehicleEntry, Details

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
        fields = ['id', 'type_vehicle', 'price', 'parking', 'is_reservation', 'is_pricehour', 'created_at', 'updated_at']


class PriceHourSerializer(ModelSerializer):
    class Meta:
        model = PriceHour
        fields = '__all__'
        extra_kwargs = {
            'start_time': {'required': False},
            'end_time': {'required': False},
            'total_time': {'required': False},
            'price': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
        }




class VehicleEntrySerializer(ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = ['id','vehicle', 'user', 'parking','is_reserva','details']

class DetailsSerializer(ModelSerializer):
    class Meta:
        model = Details
        fields = ['id', 'starttime', 'endtime', 'totalamount','price', 'extratime']
