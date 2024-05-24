from django.urls import path
from reserva.tasks import DailyTaskScheduler
from reserva.views import ReservationApiView, ReservationDetailApiView, ReservationUserDetailApiView, ParkingEarningsView

urlpatternsReservation= [
    path('reservations/', ReservationApiView.as_view()),
    path('reservations/<int:id>/', ReservationDetailApiView.as_view()),
    path('reservations/user/<int:userID>/', ReservationUserDetailApiView.as_view()),
    path('parking-earnings/', ParkingEarningsView.as_view(), name='parking-earnings'),
]

scheduler = DailyTaskScheduler()
scheduler.start()
