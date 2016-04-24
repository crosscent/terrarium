"""
This module hosts all the basic calculations that can be done, basically
anything that does not require database queries
"""

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from terrarium.utility.pot import circular_pot_calculation

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

        Get args:
            pot_radius: Radius of a pot
            seed_radius: Optimal radius of a cluster of seeds

        Returns:
            A integer of the optimal number of clusters or an error message if
            not all parameters are given
        """
        pot_radius = request.GET.get('pot_radius', None)
        seed_radius = request.GET.get('seed_radius', None)

        # check to see if all parameters are met
        if not pot_radius or not seed_radius:
            return Response("Please specify pot_radius, and seed_radius in your parameters")

        # calculate number of clusters
        return Response(circular_pot_calculation(pot_radius, seed_radius))
