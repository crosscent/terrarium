from django.contrib import admin

from terrarium.geomap import models as geomap_models

admin.site.register(geomap_models.Place)
admin.site.register(geomap_models.PlacePolygon)

