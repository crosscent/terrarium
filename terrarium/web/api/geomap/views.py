# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
This module contains all the views related to the app geomap
"""
import json
import requests
import urllib

from django.utils.encoding import iri_to_uri
from django.utils.encoding import uri_to_iri

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from terrarium.geomap.models import Place

from terrarium.web.api.geomap.etl import nominatim_to_place
from terrarium.web.api.geomap.serializers import PlaceSerializer

class PlaceViewSet(viewsets.ViewSet):
    """
    This viewest is responsible for the ``geomap`` endpoint.
    """
    
    def list(self, request):
        """
        GET method implementation of listing all the ``Place`` models
        
        Instead of listing all of the models, we are only going to display the
        last 10 updated ``Place``
        """
        query = Place.objects.order_by('-last_updated')[:10]
        serializer = PlaceSerializer(query, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        GET method implementation of retrieving details of a ``Place`` model

        Retrieve Place by osm_id instead of pk becaues this is more universal
        """
        try:
            place = Place.objects.get(osm_id=pk)
        except Place.DoesNotExist:
            return Response("osm id {0} does not exist".format(pk),
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST implementation of creating a new ``Place``
        """

        # perform ETL on the data. if no polygons provided, make a request to
        # polygons.openstreetmap.fr/get_geojson.py to retrieve GEOJson
        data = request.data
        osm_url = 'http://polygons.openstreetmap.fr/get_geojson.py'
        if 'polygons' in data and len(data['polygons']):
            pass
        else:
            response = requests.get("{0}?id={1}".format(osm_url, data['osm_id']))
            response = json.loads(response.text)
            data['polygons'] = []
            data['polygons'].append({'polygon': response['geometries'][0]})
        
        serializer = PlaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def search(self, request):
        """
        GET implementation of searching for city boundary
        
        This view requires ``query`` to be defined in the GET variables, and it
        uses ``query`` to search in Nominatim on OSM.

        Returns a properly formatted PlaceSerializer JSON
        """
        
        # Nominatim Usage Policy
        # http://wiki.openstreetmap.org/wiki/Nominatim_usage_policy

        if not request.GET.get('query', None):
            # HTTP400 is used because a more suitable HTTP422 isn't available.
            # Follow Google's Geocoding status when failed to meet parameter
            # requiremenets
            return Response("Please define query in your parameters",
                            status=status.HTTP_400_BAD_REQUEST)

        # define variables for requests, and return the response.
        request_header = {'User-Agent': 'BetterMatter.com'}
        request_parameters = urllib.urlencode({'q': request.GET['query'].encode('utf-8'),
                                            'format': 'json',
                                            'polygon': 1,
                                            'addressdetails': 1})
        request_url = "http://nominatim.openstreetmap.org/search?{0}".format(request_parameters)
 
        response = requests.get(request_url, headers=request_header).text
        response = json.loads(response)
        
        # Result has been retrieved from Nominatim. Thank you Nominatim OSM!!
        # Let's do some filtering work on the result set

        # Iterate through the result set, and return the first result that
        # meets the requirement. Nominatim has already ranked the resultset for
        # us. Thank you Nominatim OSM again!
        for osm_data in response:
            if osm_data.get('osm_type', None) == 'relation':
                return Response(nominatim_to_place(osm_data), status=status.HTTP_200_OK)

        # No result fits the filter, return the first result or return error if
        # no result was provided by Nominatim
        if len(response):
            return Response(nominatim_to_place(response[0]), status=status.HTTP_200_OK)
        return Response(u'No result for {0}'.format(request.GET['query']),
                        status=status.HTTP_200_OK)
