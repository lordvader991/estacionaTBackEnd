from django.urls import path

from extratime.views import ExtraTimeApiView, ExtraTimeDetailApiView


urlpattern_extratime= [
    path('extratime/', ExtraTimeApiView.as_view()),
    path('extratime/<int:id>/', ExtraTimeDetailApiView.as_view()),
   
]
