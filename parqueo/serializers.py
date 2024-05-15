from rest_framework.serializers import ModelSerializer
from parqueo.models import  Parking, Address, OpeningHours, Price, PriceHour, VehicleEntry, Details
from parqueo.models import Parking, Address, OpeningHours, Price, VehicleEntry, Details
from vehiculos.serializers import TypeVehicleSerializer, VehicleSerializer

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
            'day': {'required': False},
            'open_time': {'required': False},
            'close_time': {'required': False},
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
        fields = ['id','type_vehicle','is_entry_fee' ,'price', 'parking', 'is_reservation', 'is_pricehour', 'price_hour']

    def create(self, validated_data):
        price_hour_data = validated_data.pop('price_hour', None)
        price = Price.objects.create(**validated_data)

        if price_hour_data:
            PriceHour.objects.create(price=price, **price_hour_data)

        return price

class VehicleEntrySerializer(ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = ['id','vehicle', 'user', 'parking','is_reserva','phone','is_userexternal']
        extra_kwargs = {
            'vehicle': {'required': False},
            'user': {'required': False},
            'parking': {'required': False},
            'is_reserva': {'required': False},
            'phone': {'required': False},
            'is_userexternal': {'required': False},
        }

class VehicleEntryDataSerializer(ModelSerializer):
    vehicle = VehicleSerializer()
    class Meta:
        model = VehicleEntry
        fields = ['id', 'vehicle', 'user', 'parking', 'is_reserva', 'phone', 'is_userexternal']
        extra_kwargs = {
            'vehicle': {'required': False},
            'user': {'required': False},
            'parking': {'required': False},
            'is_reserva': {'required': False},
            'phone': {'required': False},
            'is_userexternal': {'required': False},
        }


class DetailsSerializer(ModelSerializer):
    class Meta:
        model = Details
        fields = ['id', 'starttime', 'endtime', 'totalamount','price', 'extratime', 'vehicle_entry']
        extra_kwargs = {
            'starttime': {'required': False},
            'endtime': {'required': False},
            'totalamount': {'required': False},
            'price': {'required': False},
            'extratime': {'required': False},
            'vehicle_entry': {'required': False},
        }
