# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from terrarium.plants.models import Plant

from terrarium.web.api.plants.serializers import PlantSerializer

class PlantViewSet(viewsets.ViewSet):
    """
    This viewset is responsible for the ``plant`` endpoint.
    """

    def list(self, request):
        """
        GET method implementation of listing the latest ``Plant`` models

        Instead of listing all of the models, we are only going to display the
        last 10
        """
        query = Plant.objects.order_by('-id')[:10]
        serializer = PlantSerializer(query, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def search(self, request):
        """
        GET method implementation of listing all the ``Plant`` models that meet
        the requirement
        """

        # Right now, only accept queries that have a single value to the key,
        # as this will make things easier to deal with
        query_dict = dict(request.GET)
        for key, value in query_dict.iteritems():
            if len(value) > 1:
                query_dict.pop('key')
            else:
                if key == 'accepted' or key =='public':
                    if value[0] == 'True':
                        query_dict[key] = True
                    else:
                        query_dict[key] = False
                else:
                    query_dict[key] = value[0]

        query = Plant.objects.filter(**query_dict)[:10]
        serializer = PlantSerializer(query,many=True)
        return Response(serializer.data)
