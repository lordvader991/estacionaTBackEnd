from django.urls import path
from reserva.tasks import DailyTaskScheduler, initialize_scheduler
from reserva.views import MonthlyEarningsView, ParkingStatisticsView, PopularPricesView, ReservationApiView, ReservationDetailApiView, ReservationPayment, ReservationUserDetailApiView, ParkingEarningsView

urlpatternsReservation= [
    path('reservations/', ReservationApiView.as_view()),
    path('reservations/<int:id>/', ReservationDetailApiView.as_view()),
    path('reservations/user/<int:userID>/', ReservationUserDetailApiView.as_view()),
    path('parking-earnings/<int:parking_id>/', ParkingEarningsView.as_view(), name='parking-earnings'),
    #Estadisticas
     path('reservations/payment/<int:id>/', ReservationPayment.as_view()),
      path('parking/<int:parking_id>/statistics/', ParkingStatisticsView.as_view(), name='parking_statistics_ocupation'),
    path('parking/<int:parking_id>/monthly-earnings/', MonthlyEarningsView.as_view(), name='monthly_earnings'),
    path('parking/<int:parking_id>/popular-prices/', PopularPricesView.as_view(), name='popular_prices'),
]


scheduler = initialize_scheduler()
daily_task_scheduler = DailyTaskScheduler()