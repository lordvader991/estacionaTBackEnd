from django.urls import path
from bd.views import PersonApiView, PersonDetailApiView, UserApiView, UserDetailApiView

urlpatterns_person = [
    path('v1/person', PersonApiView.as_view()),
    path('v1/person/<int:id>/', PersonDetailApiView.as_view()),
    path('v1/user', UserApiView.as_view()),
    path('v1/user/<int:id>/', UserDetailApiView.as_view())  # Cambia 'person' a 'user' aquí
]
