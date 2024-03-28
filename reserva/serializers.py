from rest_framework.serializers import ModelSerializer
from reserva.models import ExtraTime


class ExtraTimeSerializer(ModelSerializer):
    class Meta:
        model = ExtraTime
        fields = ['id', 'start_time', 'end_time', 'duration']


