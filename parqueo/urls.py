from django.urls import path
from parqueo.views import AddressParkingView, ParkingApiView, ParkingDetailApiView, AddressApiView, AddressDetailApiView, OpeningHoursApiView, OpeningHoursDetailApiView, ParkingView, PriceDetailApiView, PriceApiView, PriceParkingApiView, VehicleEntryApiView, VehicleEntryDetailApiView, DetailsApiView, DetailsDetailApiView, DetailsApiCustomView
urlpatterns_parqueos = [
    path('parking/<int:id>/', ParkingDetailApiView.as_view()),
    path('parking/', ParkingApiView.as_view()),
    path('parking/user/', ParkingView.as_view()),
    path('address/<int:id>/', AddressDetailApiView.as_view()),
    path('address/parking/<int:parkingID>/', AddressParkingView.as_view()),
    path('address/', AddressApiView.as_view()),
    path('openinghours/<int:id>/', OpeningHoursDetailApiView.as_view()),
    path('openinghours/', OpeningHoursApiView.as_view()),
    path('price/<int:id>/', PriceDetailApiView.as_view()),
    path('price/parking/<int:parkingID>/', PriceParkingApiView.as_view()),
    path('price/', PriceApiView.as_view()),
    path('vehicleentry/<int:id>/', VehicleEntryDetailApiView.as_view()),
    path('vehicleentry/', VehicleEntryApiView.as_view()),
    path('Details/<int:id>/', DetailsDetailApiView.as_view()),
    path('Details/', DetailsApiView.as_view()),
    path('DetailsCustom/save_details', DetailsApiCustomView.as_view(), name='save_details')

]
