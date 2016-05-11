from django.test import TestCase

from rest_framework.test import APIClient

class PlaceQueryTest(TestCase):
    """Tests multiple scenarios for the GET implementation at /api/place/search
    """
    def test_none_existing_place(self):
        """Test search query for a non-existent place

        Should return an error message
        """
        pass

    def test_place_with_polygon(self):
        """Test search query for a Nominatim result that contains polypoints
        
        Should return JSON with GEOJSONized polypoints
        """
        pass

    def test_place_with_no_polygon(self):
        """Test search query for a Nominatim result that does not contain
        polypoints.

        Should return JSON with GEOJSON from polygons.openstreetmap.fr
        """
        pass

class PlaceCreationTest(TestCase):
    """Tests multiple scenarios for the POST implemenation at /api/place/
    """
    def test_large_int(self):
        """Test large place_id, and large_osm_id
        
        BigIntegers should be able to handle up to 9223372036854775807
        """
        pass


    def test_place_creation_unicode(self):
        """Test Place creation using unicode data

        Display name should be correct
        """
        pass

    def test_place_creation_with_query_data(self):
        """Test Place creation using the data returned on /api/place/search
        """

    def test_place_creation_invalid_data(self):
        """Test Place creation with results lacking

        Should return an error message
        """
        pass

    def test_place_creation_invalid_polygon(self):
        """Test Place creation with an invalid polygon

        Should return an error message
        """
        pass

class PlaceRetrieveTest(TestCase):
    """Tests multiple scenarios for the GET implementation at /api/place/id/
    """
    def test_unicode(self):
        """Test unicode result

        JSON should be properly encoded
        """
        pass

    def test_non_existing_id(self):
        """Test an OSM id that doesn't exist

        Should return error message
        """

class PlaceListTest(TestCase):
    """Tests multiple scenarios for teh GET implementation at /api/place/
    """

    def test_unicode(self):
        """Test unicode result

        JSON should be properly encoded
        """
        pass

