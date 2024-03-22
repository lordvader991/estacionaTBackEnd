from django.urls import path
from reserva.views import ExtraTimeApiView, ExtraTimeDetailApiView, ReservationApiView, ReservationDetailApiView

urlpattern_reservas = [
    path('extratime/', ExtraTimeApiView.as_view()),
    path('extratime/<int:id>/', ExtraTimeDetailApiView.as_view()),
    path('reservation/', ReservationApiView.as_view()),
    path('reservation/<int:id>/', ReservationDetailApiView.as_view()),
]
