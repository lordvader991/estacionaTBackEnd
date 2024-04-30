"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.urls import urlpatterns_user
from vehiculos.urls import urlpatterns_vehiculos
from parqueo.urls import urlpatterns_parqueos
from extratime.urls import urlpattern_extratime
from reserva.urls import urlpatternsReservation
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/user/', include(urlpatterns_user)),
    path('api/v2/vehicles/', include(urlpatterns_vehiculos)),
    path('api/v2/parking/', include(urlpatterns_parqueos)),
    path('api/v2/extratime/', include(urlpattern_extratime)),
    path('api/v2/reservation/', include(urlpatternsReservation)),
]
