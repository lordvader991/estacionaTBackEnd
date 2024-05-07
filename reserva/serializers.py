from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    extra_time = serializers.IntegerField(required=False)
    class Meta:
        model = Reservation
        fields = ['id', 'start_time', 'end_time', 'total_amount', 'price', 'extra_time','reservation_date','user']
