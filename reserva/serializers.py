from rest_framework.serializers import ModelSerializer
from reserva.models import ExtraTime, Reservation


class ExtraTimeSerializer(ModelSerializer):
    class Meta:
        model = ExtraTime
        fields = ['id', 'start_time', 'end_time', 'duration']


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'starttime', 'endtime', 'totalamount', 'date', 'vehicle', 'price', 'extratime']
