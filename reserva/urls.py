from django.urls import path
from reserva.tasks import DailyTaskScheduler
from reserva.views import ReservationApiView, ReservationDetailApiView

urlpatternsReservation= [
    path('reservations/', ReservationApiView.as_view()),
    path('reservations/<int:id>/', ReservationDetailApiView.as_view()),
]

scheduler = DailyTaskScheduler()
scheduler.start()