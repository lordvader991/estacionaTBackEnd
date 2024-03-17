from django.urls import path
from bd.views import PersonApiView, PersonDetailApiView


urlpatterns_person = [
    path('v1/person', PersonApiView.as_view()),
    path('v1/person/<int:id>/', PersonDetailApiView.as_view())
]