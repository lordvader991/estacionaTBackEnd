from rest_framework import serializers

from parqueo.models import VehicleEntry
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    extra_time = serializers.IntegerField(required=False)
    vehicle_entry = serializers.PrimaryKeyRelatedField(queryset=VehicleEntry.objects.all(), required=False)

    class Meta:
        model = Reservation
        fields = ['id', 'start_time', 'end_time', 'total_amount', 'price', 'extra_time', 'reservation_date', 'user', 'vehicle_entry']

class ParkingEarningsSerializer(serializers.Serializer):
    parking = serializers.IntegerField()
    total_earnings = serializers.FloatField()
    vehicle_count = serializers.IntegerField()
