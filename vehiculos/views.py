from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from vehiculos.models import TypeVehicle, Vehicle
from vehiculos.serializers import TypeVehicleSerializer, VehicleSerializer

class TypeVehicleApiView(APIView):
    def get(self, request):
        serializer = TypeVehicleSerializer(TypeVehicle.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=TypeVehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class TypeVehicleDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return TypeVehicle.objects.get(pk=pk)
        except TypeVehicle.DoesNotExist:
            return None

    def get(self, request, id):
        TypeVehicle = self.get_object(id)
        if TypeVehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TypeVehicleSerializer(TypeVehicle)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        TypeVehicle = self.get_object(id)
        if TypeVehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TypeVehicleSerializer(TypeVehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        TypeVehicle = self.get_object(id)
        if TypeVehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        TypeVehicle.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

class VehicleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        userID = request.user.id
        vehicleByUser = Vehicle.objects.filter(user=userID)
        if not vehicleByUser.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicleByUser, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    def post(self,request):
        serializer=VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class VehicleDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return None

    def get(self, request, id):
        Vehicle = self.get_object(id)
        if Vehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(Vehicle)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, id):
        Vehicle = self.get_object(id)
        if Vehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(Vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, id):
        Vehicle = self.get_object(id)
        if Vehicle is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Vehicle.delete()
        response_data = {'deleted': True}
        return Response(status=status.HTTP_200_OK, data=response_data)

class VehicleUserApiView(APIView):

    def get(self, request,userID):
        vehicleByUser = Vehicle.objects.filter(user=userID)
        if not vehicleByUser.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VehicleSerializer(vehicleByUser, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
