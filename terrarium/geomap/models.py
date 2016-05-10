from django.db import models
from django.contrib.gis.db import models as geo_models

class Place(models.Model):
    """A summarization of each place in OSM

    A summary of details excluding boundary polygons for a specific place given
    by nomination.openstreeetmap.org
    """
    display_name = models.CharField(max_length=255)
    osm_id = models.PositiveIntegerField(unique=True)
    place_id = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    NONE = 0
    NODE = 1
    WAY = 2
    RELATION = 3

    OSM_TYPES = ((NONE, 'None'),
                  (NODE, 'Node'),
                  (WAY, 'Way'),
                  (RELATION, 'Relation'))

    osm_type = models.IntegerField(choices=OSM_TYPES, default=NONE)

    def __str__(self):
        """Return the osm_id and name of the place
        """
        return "{0}, {1}".format(self.osm_id, self.display_name)

class PlacePolygon(models.Model):
    """Bounday Polygon for each place in OSM

    An individual ``polygon`` for shaping each Place.

    Each PlacePolygon is always a member of Place, which groups all the related
    information regarding each place. The simplicity field refers to the value
    passed to GEOSGeometry.simplify(tolerance=simplicity)
    """
    place = models.ForeignKey(Place, related_name='polygons')
    polygon = geo_models.MultiPolygonField(blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)
    simplicity = models.IntegerField(default=0)

    def __str__(self):
        """Return the osm_id, the place name, and the simplicity of the polygon
        """
        return "{0}, {1}, {2}".format(self.place.osm_id,
                                      self.place.display_name,
                                      self.simplicity)
