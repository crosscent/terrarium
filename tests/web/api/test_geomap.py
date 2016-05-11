# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.utils.encoding import iri_to_uri
from django.utils.encoding import uri_to_iri

from rest_framework.test import APIClient

class PlaceQueryTest(TestCase):
    """Tests multiple scenarios for the GET implementation at /api/place/search
    """
    url = '/api/place/search/'
    def test_none_existing_place(self):
        """Test search query for a non-existent place

        Should return an error message
        """
        client = APIClient()
        location_name = 'lala this place doesn\'t exist'
        response = client.get("{0}?query={1}".format(self.url, location_name))
        self.assertEqual(response.data['detail'], "No result for {0}".format(location_name))

    def test_place_with_polygon(self):
        """Test search query for a Nominatim result that contains polypoints
        
        Should return JSON with GEOJSONized polypoints
        """
        client = APIClient()
        location_name = 'Vancouver, BC'
        response = client.get("{0}?query={1}".format(self.url, location_name))
        self.assertEqual(len(response.data['polygons']), 1)

    def test_place_with_no_polygon(self):
        """Test search query for a Nominatim result that does not contain
        polypoints.

        Should return JSON with GEOJSON from polygons.openstreetmap.fr
        """
        client = APIClient()
        location_name = 'New York, New York'
        response = client.get("{0}?query={1}".format(self.url, location_name))
        self.assertEqual(len(response.data['polygons']), 0)
    

class PlaceCreationTest(TestCase):
    """Tests multiple scenarios for the POST implemenation at /api/place/
    """
    search_url = '/api/place/search/'
    base_url = '/api/place/'

    def test_large_int(self):
        """Test large place_id, and large_osm_id
        
        BigIntegers should be able to handle up to 9223372036854775807

        PositiveIntegerField and IntegerField handles up to 2147483647
        """
        
        # Houston Texas has a place id of 2598942101, which is more than what
        # an IntegerField can handle
        client = APIClient()
        location_name = 'Houston, Texas'
        
        # search for Houston Texas, POST the returned data, the GET the osm_id
        # returned
        nominatim_result = client.get("{0}?query={1}".format(self.search_url,
                                                             location_name))
        self.assertTrue(int(nominatim_result.data['place_id']) > 2147483647)

        create_result = client.post("{0}".format(self.base_url),
                                    nominatim_result.data,
                                    format='json')
        self.assertTrue(int(nominatim_result.data['osm_id']) == int(create_result.data['osm_id']))

        retrieve_result = client.get("{0}{1}/".format(self.base_url,
                                                     create_result.data['osm_id']))
        self.assertTrue('osm_id' in retrieve_result.data)

    def test_place_creation_unicode(self):
        """Test Place creation using unicode data

        Display name should be correct
        """
        client = APIClient()
        location_name = 'Grand-Mère'

        # search for the location, POST the returned data, and GET the osm_id
        # returned

        nominatim_result = client.get("{0}".format(self.search_url),
                                      {'query': location_name})
        create_result = client.post("{0}".format(self.base_url),
                                    nominatim_result.data,
                                    format='json')
        retrieve_result = client.get("{0}{1}/".format(self.base_url,
                                                      create_result.data['osm_id']))
        self.assertTrue(location_name in retrieve_result.data['display_name'])

    def test_place_creation_invalid_data(self):
        """Test Place creation with results lacking

        Should return an error message
        """
        client = APIClient()
        data = {'osm_type': 3,
                'place_id': "2598942101",
                'display_name': 'Houston, Texas',
                'polygons': [],}
        create_result = client.post('{0}'.format(self.base_url),
                                    data,
                                    format='json')
        self.assertFalse('osm_id' in create_result.data)

    def test_place_creation_invalid_polygon(self):
        """Test Place creation with an invalid polygon

        Should return an error message
        """
        # https://knowledge.safe.com/articles/21674/invalid-ogc-geometry-examples.html
        # has a list of useful invalid polygons for testing
        # Currently we are testing Too Few Points
        client = APIClient()
        data = {'osm_type': 3,
                'osm_id': '252345',
                'place_id': '2598942101',
                'display_name': 'Houston, Texas',
                'polygons': [
                    {'polygon': {
                        'type': 'MultiPolygon',
                        'coordinates': [
                            [
                                [
                                    [-123.2248817, 49.273306],
                                ]    
                            ]    
                        ]
                    }}
                ]}
        create_result = client.post('{0}'.format(self.base_url),
                                    data,
                                    format='json')
        self.assertTrue('Invalid format' in create_result.data['polygons'][0]['polygon'][0])

    def test_place_creation_invalid_polygon_invalid_osmid(self):
        """Test Place with invalid polygon and invalid osmid
        
        Should return an error message
        """
        client = APIClient()
        data = {'osm_type': 3,
                'osm_id': 8923597234985,
                'place_id': '532452345523',
                'display_name': 'Houston, Texas',
                'polygons': [
                    {'polygon': {
                        'type': 'MultiPolygon',
                        'coordinates': [
                            [
                                [
                                    [-123.2248817, 49.273306],
                                ]    
                            ]    
                        ]
                    }}
                ]}
        
        create_result = client.post('{0}'.format(self.base_url),
                                    data,
                                    format='json')
        self.assertTrue('Invalid format' in create_result.data['polygons'][0]['polygon'][0])

class PlaceRetrieveTest(TestCase):
    """Tests multiple scenarios for the GET implementation at /api/place/id/
    """
    base_url = '/api/place/'

    def test_non_existing_id(self):
        """Test an OSM id that doesn't exist

        Should return error message
        """
        client = APIClient()
        retrieve_result = client.get('{0}{1}/'.format(self.base_url, 1))
        self.assertTrue('detail' in retrieve_result.data)
