from django.urls import path
from accounts.views import LoginAPIView, UserDetailApiView ,SignupAPIView

urlpatterns_user = [
    path('login/', LoginAPIView.as_view()),
    path('signup/',SignupAPIView.as_view()),
    path('users/<int:id>/', UserDetailApiView.as_view()),
]
