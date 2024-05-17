from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from parqueo.serializers import VehicleEntrySerializer
from reserva.models import Reservation
from reserva.serializers import ReservationSerializer
from datetime import date, datetime,timedelta
from .tasks import DailyTaskScheduler
from django.db import transaction

class ReservationApiView(APIView):
    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self, request, *args, **kwargs):
        return self.save_details(request, *args, **kwargs)

    def save_details(self, request, *args, **kwargs):
        with transaction.atomic():
            reservation_data = request.data.get('reservation')
            vehicle_entry_data = request.data.get('vehicle_entry')
      
            vehicle_entry_data['is_reserva'] = True

            vehicle_entry_serializer = VehicleEntrySerializer(data=vehicle_entry_data)
            vehicle_entry_serializer.is_valid(raise_exception=True)
            vehicle_entry = vehicle_entry_serializer.save()
        
            reservation_serializer = ReservationSerializer(data=reservation_data)
            reservation_serializer.is_valid(raise_exception=True)
        
            reservation_serializer.validated_data['vehicle_entry'] = vehicle_entry
            reservation = reservation_serializer.save()

            if reservation_serializer.validated_data.get('reservation_date') == date.today():
                DailyTaskScheduler().create_task(reservation)

            return Response(status=status.HTTP_201_CREATED, data={
            'reservation': reservation_serializer.data,
            'vehicle_entry': vehicle_entry_serializer.data,
            })

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

class ReservationUserDetailApiView(APIView):
    def get(self, request, userID):
        reservations = Reservation.objects.filter(user=userID)
        if not reservations:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



