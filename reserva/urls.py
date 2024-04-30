from django.urls import path
from reserva.views import ReservationApiView, ReservationDetailApiView
from . import tasks
urlpatternsReservation= [
    path('reservations/', ReservationApiView.as_view()),
    path('reservations/<int:id>/', ReservationDetailApiView.as_view()),
]

tasks.startScheduler()