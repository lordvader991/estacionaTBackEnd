from rest_framework.serializers import ModelSerializer
from vehiculos.models import  TypeVehicle, Vehicle

class TypeVehicleSerializer(ModelSerializer):
    class Meta:
        model = TypeVehicle
        fields = ['id','name', 'description']

class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','brand', 'model', 'registration_plate', 'type_vehicle', 'user']
