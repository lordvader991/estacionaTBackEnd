from django.urls import path
from accounts.views import LoginAPIView, MobileTokenListCreateAPIView, MobileTokenRetrieveUpdateDestroyAPIView, UserDetailApiView ,SignupAPIView

urlpatterns_user = [
    path('login/', LoginAPIView.as_view()),
    path('signup/',SignupAPIView.as_view()),
    path('users/<int:id>/', UserDetailApiView.as_view()),
    path('users/mobile-tokens/', MobileTokenListCreateAPIView.as_view()),
    path('users/mobile-tokens/<int:pk>/', MobileTokenRetrieveUpdateDestroyAPIView.as_view()),
]
