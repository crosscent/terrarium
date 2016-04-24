from django.conf.urls import include
from django.conf.urls import url

from rest_framework import routers

from terrarium.web.api import calculation

default_router = routers.DefaultRouter()

default_router.register(r'calculation',
                        calculation.CalculationViewSet,
                        'Calculation')

urlpatterns = [
    url(r'^', include(default_router.urls)),       
]
