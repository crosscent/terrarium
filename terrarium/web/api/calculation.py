"""
This module hosts all the basic calculations that can be done, basically
anything that does not require database queries
"""
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

class CalculationViewSet(viewsets.ViewSet):
    """
    This viewset is responsible for the ``calculation`` endpoint.
    """

    def list(self, request):
        """
        GET method implementation of listing all possible calculations
        """
        functions = {}
        functions['circular_pot'] = "Calculate the number of seed clusters suitable for a certain pot size"
        return Response(functions)

    @list_route(methods=['get'])
    def circular_pot(self, request):
        """
        GET method implementation of calculating pot size
        """
        return Response("pot size calculation")

