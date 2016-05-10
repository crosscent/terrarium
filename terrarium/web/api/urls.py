from django.conf.urls import include
from django.conf.urls import url

from rest_framework import routers

from terrarium.web.api import authentication
from terrarium.web.api import calculation
from terrarium.web.api.geomap import views as geomap_views 
authentication_router = routers.SimpleRouter()

default_router = routers.DefaultRouter()

default_router.register(
    r'account',
    authentication.UserView,
    'account'
)

default_router.register(
    r'calculation',
    calculation.CalculationViewSet,
    'Calculation'
)

default_router.register(
    r'place',
    geomap_views.PlaceViewSet,
    'Place'
)

urlpatterns = [
    url(r'^',
        include(default_router.urls)),       
]
