from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from reserva.models import ExtraTime, Reservation
from reserva.serializers import ExtraTimeSerializer, ReservationSerializer


class ExtraTimeApiView(APIView):
    def get(self, request):
        serializer = ExtraTimeSerializer(ExtraTime.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=ExtraTimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class ExtraTimeDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return ExtraTime.objects.get(pk=pk)
        except ExtraTime.DoesNotExist:
            return None

    def get(self, request, id):
        ExtraTime = self.get_object(id)
        if ExtraTime is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExtraTimeSerializer(ExtraTime)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        ExtraTime = self.get_object(id)
        if ExtraTime is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExtraTimeSerializer(ExtraTime, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        ExtraTime = self.get_object(id)
        if ExtraTime is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ExtraTime.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

class ReservationApiView(APIView):
    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class ReservationDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, id):
        Reservation = self.get_object(id)
        if Reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(Reservation)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Reservation = self.get_object(id)
        if Reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(Reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Reservation = self.get_object(id)
        if Reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Reservation.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

