from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from parqueo.models import Parking, Address, OpeningHours, Price, VehicleEntry, Details
from parqueo.serializers import ParkingSerializer, AddressSerializer,OpeningHoursSerializer, PriceSerializer, VehicleEntrySerializer, DetailsSerializer

""" parking """
class ParkingApiView(APIView):
    def get(self, request):
        serializer = ParkingSerializer(Parking.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = ParkingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        user = serializer.validated_data.get('user')
        user.rol_usuario = True
        user.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class ParkingDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Parking.objects.get(pk=pk)
        except Parking.DoesNotExist:
            return None

    def get(self, request, id):
        Parking = self.get_object(id)
        if Parking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParkingSerializer(Parking)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Parking = self.get_object(id)
        if Parking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParkingSerializer(Parking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Parking = self.get_object(id)
        if Parking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Parking.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

class ParkingView(APIView):
    def get(self, request,userID):
        parkingsByUser = Parking.objects.filter(user=userID)
        if not parkingsByUser.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParkingSerializer(parkingsByUser, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

""" address"""

class AddressApiView(APIView):
    def get(self, request):
        serializer = AddressSerializer(Address.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class AddressDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return None

    def get(self, request, id):
        Address = self.get_object(id)
        if Address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(Address)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Address = self.get_object(id)
        if Address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(Address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Address = self.get_object(id)
        if Address is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Address.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)


""" openingHours """

class OpeningHoursApiView(APIView):
    def get(self, request):
        serializer = OpeningHoursSerializer(OpeningHours.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=OpeningHoursSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class OpeningHoursDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return OpeningHours.objects.get(pk=pk)
        except OpeningHours.DoesNotExist:
            return None

    def get(self, request, id):
        OpeningHours = self.get_object(id)
        if OpeningHours is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OpeningHoursSerializer(OpeningHours)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        OpeningHours = self.get_object(id)
        if OpeningHours is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OpeningHoursSerializer(OpeningHours, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        OpeningHours = self.get_object(id)
        if OpeningHours is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        OpeningHours.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)


""" Price"""
class PriceApiView(APIView):
    def get(self, request):
        serializer = PriceSerializer(Price.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=PriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class PriceDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Price.objects.get(pk=pk)
        except Price.DoesNotExist:
            return None

    def get(self, request, id):
        Price = self.get_object(id)
        if Price is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PriceSerializer(Price)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Price = self.get_object(id)
        if Price is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PriceSerializer(Price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Price = self.get_object(id)
        if Price is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Price.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)


""" Vehicle Entry """
class VehicleEntryApiView(APIView):
    def get(self, request):
        serializer = VehicleEntrySerializer(VehicleEntry.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=VehicleEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class VehicleEntryDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return VehicleEntry.objects.get(pk=pk)
        except VehicleEntry.DoesNotExist:
            return None

    def get(self, request, id):
        VehicleEntry = self.get_object(id)
        if VehicleEntry is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleEntrySerializer(VehicleEntry)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        VehicleEntry = self.get_object(id)
        if VehicleEntry is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleEntrySerializer(VehicleEntry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        VehicleEntry = self.get_object(id)
        if VehicleEntry is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        VehicleEntry.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)


""" DetailsEntry"""
class DetailsApiView(APIView):
    def get(self, request):
        serializer = DetailsSerializer(Details.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=DetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class DetailsDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Details.objects.get(pk=pk)
        except Details.DoesNotExist:
            return None

    def get(self, request, id):
        Details = self.get_object(id)
        if Details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DetailsSerializer(Details)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Details = self.get_object(id)
        if Details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DetailsSerializer(Details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Details = self.get_object(id)
        if Details is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Details.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)
