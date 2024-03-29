from django.urls import path
from parqueo.views import ParkingApiView, ParkingDetailApiView, AddressApiView, AddressDetailApiView, OpeningHoursApiView, OpeningHoursDetailApiView, ParkingView, PriceDetailApiView, PriceApiView, VehicleEntryApiView, VehicleEntryDetailApiView, DetailsApiView, DetailsDetailApiView
urlpatterns_parqueos = [
    path('parking/<int:id>/', ParkingDetailApiView.as_view()),
    path('parking/', ParkingApiView.as_view()),
    path('parking/user/<int:userID>/', ParkingView.as_view()),
    path('address/<int:id>/', AddressDetailApiView.as_view()),
    path('address/', AddressApiView.as_view()),
    path('openinghours/<int:id>/', OpeningHoursDetailApiView.as_view()),
    path('openinghours/', OpeningHoursApiView.as_view()),
    path('price/<int:id>/', PriceDetailApiView.as_view()),
    path('price/', PriceApiView.as_view()),
    path('vehicleentry/<int:id>/', VehicleEntryDetailApiView.as_view()),
    path('vehicleentry/', VehicleEntryApiView.as_view()),
    path('Details/<int:id>/', DetailsDetailApiView.as_view()),
    path('Details/', DetailsApiView.as_view()),

]
