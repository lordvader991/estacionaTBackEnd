from rest_framework.serializers import ModelSerializer
from parqueo.models import  Parking, Address, OpeningHours, Price, PriceHour, VehicleEntry, Details
from parqueo.models import Parking, Address, OpeningHours, Price, VehicleEntry, Details
from vehiculos.serializers import TypeVehicleSerializer

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id','name', 'capacity', 'phone', 'email', 'user', 'spaces_available', 'url_image', 'description']
        extra_kwargs = {
            'phone': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'user': {'required': False},
            'spaces_available': {'required': False},
            'url_image': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
        }

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','city', 'street', 'longitude', 'latitude', 'parking']
        extra_kwargs = {
            'city': {'required': False, 'allow_blank': True},
            'street': {'required': False, 'allow_blank': True},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'parking': {'required': False},
        }

class OpeningHoursSerializer(ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ['id','day', 'open_time', 'close_time', 'parking']
        extra_kwargs = {
            'day': {'required': False, 'allow_blank': True},
            'open_time': {'required': False, 'allow_blank': True},
            'close_time': {'required': False, 'allow_blank': True},
            'parking': {'required': False},
        }



class PriceHourSerializer(ModelSerializer):
    class Meta:
        model = PriceHour
        fields = '__all__'
        extra_kwargs = {
            'start_time': {'required': False},
            'end_time': {'required': False},
            'total_time': {'required': False},
            'price': {'required': False},
        }

class PriceSerializer(ModelSerializer):
    price_hour = PriceHourSerializer(required=False)
 
    class Meta:
        model = Price
        fields = ['type_vehicle', 'price', 'parking', 'is_reservation', 'is_pricehour', 'price_hour']

    def create(self, validated_data):
        price_hour_data = validated_data.pop('price_hour', None)
        price = Price.objects.create(**validated_data)

        if price_hour_data:
            PriceHour.objects.create(price=price, **price_hour_data)

        return price

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
