from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reserva.models import Reservation
from reserva.serializers import ReservationSerializer
from datetime import date, datetime,timedelta
from .tasks import DailyTaskScheduler
class ReservationApiView(APIView):
    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('reservation_date') == date.today():
            DailyTaskScheduler().create_task(serializer.validated_data)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class ReservationDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        reservation = self.get_object(id)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reservation.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)
