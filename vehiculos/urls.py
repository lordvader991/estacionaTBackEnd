from django.urls import path
from vehiculos.views import TypeVehicleApiView, TypeVehicleDetailApiView, VehicleApiView, VehicleDetailApiView, VehicleUserApiView
urlpatterns_vehiculos = [
    path('typevehicle/', TypeVehicleApiView.as_view()),
    path('typevehicle/<int:id>/', TypeVehicleDetailApiView.as_view()),
    path('vehicle/<int:id>/', VehicleDetailApiView.as_view()),
    path('vehicle/', VehicleApiView.as_view()),
    path('vehicle/user/<int:userID>', VehicleUserApiView.as_view()),
]
