from django.urls import path
from accounts.views import LoginAPIView, UserDetailApiView ,SignupAPIView

urlpatterns_user = [
    path('login/', LoginAPIView.as_view()),
    path('signup/',SignupAPIView.as_view()),
    path('user/', UserDetailApiView.as_view()),
]
