from django.urls import path
from reserva.views import ExtraTimeApiView, ExtraTimeDetailApiView

urlpattern_reservas = [
    path('extratime/', ExtraTimeApiView.as_view()),
    path('extratime/<int:id>/', ExtraTimeDetailApiView.as_view()),
   
]
