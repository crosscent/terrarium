"""
This module hosts all the basic calculations that can be done, basically
anything that does not require database queries
"""
import base64
import cStringIO

from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from PIL import Image
from PIL import ImageDraw

from terrarium.utility.pot import circular_pot_calculation
from terrarium.utility.pot import rectangular_pot_calculation

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
            A dictionary of the following format
            {
                "cluster_count": number of clusters,
                "clusters": a list of cluster positions
            }
        """
        pot_radius = request.GET.get('pot_radius', None)
        seed_radius = request.GET.get('seed_radius', None)

        # check to see if all parameters are met
        if pot_radius and seed_radius:
            try:
                pot_radius = float(pot_radius)
                seed_radius = float(seed_radius)
            except ValueError:
                return Response("Please enter numbers for pot_radius, and seed_radius")
        else:
            return Response("Please specify pot_radius, and seed_radius in your parameters")

        # calculate number of clusters
        cluster_count, clusters = circular_pot_calculation(pot_radius,
                seed_radius)

        canvas_height = 500
        canvas_width = 500
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2
        ratio = canvas_height / 2 / pot_radius

        image = Image.new('RGBA', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(image)
        for cluster in clusters:
            draw.ellipse((canvas_center_x + (cluster['x'] - seed_radius) * ratio,
                           canvas_center_y + (cluster['y'] - seed_radius) * ratio,
                           canvas_center_x + (cluster['x'] + seed_radius) * ratio,
                           canvas_center_y + (cluster['y'] + seed_radius) * ratio),
                           fill="#009933")
        buffer = cStringIO.StringIO()
        image.save(buffer, "JPEG")
        image_string = base64.b64encode(buffer.getvalue())
        return Response({"cluster_count": cluster_count,
                         "clusters": clusters,
                         'image': '{0}'.format(image_string)})

    @list_route(methods=['get'])
    def rectangular_pot(self, request):
        """
        GET method implementation of calculating the number of seed clusters
        available for planting in a rectangular pot

        GET args:
            pot_length: length of a pot
            pot_width: width of a pot
            seed_radius: Optimal radius of a cluster of seeds

        Returns:
            A dictionary of the following format
            {
                "cluster_count": number of clusters,
                "clusters": a list of cluster positions
            }
        """
        pot_length = request.GET.get('pot_length', None)
        pot_width = request.GET.get('pot_width', None)
        seed_radius = request.GET.get('seed_radius', None)

        # check to see if all parameters are met
        if pot_length and pot_width and seed_radius:
            try:
                pot_length = float(pot_length)
                pot_width = float(pot_width)
                seed_radius = float(seed_radius)
            except ValueError:
                return Response("Please enter numbers for pot_length, pot_width, and seed_radius")
        else:
            return Response("Please specify pot_length, pot_width, and seed_radius in your parameters")

        # calculate the number of clusters
        cluster_count, clusters = rectangular_pot_calculation(pot_length,
                                                              pot_width,
                                                              seed_radius)
        ratio = 500 / max(pot_length, pot_width)
        canvas_height = int(pot_length * ratio)
        canvas_width = int(pot_width * ratio)

        # draw circles
        image = Image.new('RGBA', (canvas_height, canvas_width), 'white')
        draw = ImageDraw.Draw(image)
        for cluster in clusters:
            draw.ellipse(((cluster['x'] - seed_radius) * ratio,
                          (cluster['y'] - seed_radius) * ratio,
                          (cluster['x'] + seed_radius) * ratio,
                          (cluster['y'] + seed_radius) * ratio),
                           fill="#009933")

        buffer = cStringIO.StringIO()
        image.save(buffer, "JPEG")
        image_string = base64.b64encode(buffer.getvalue())
        return Response({"cluster_count": cluster_count,
                         "clusters": clusters,
                         "image": image_string})

    @list_route(methods=['get'])
    def circular_pot_image(self, request):
        """
        GET method implementation of calculating pot size

        Similar to circular_pot, but returns an image instead
        """
        pot_radius = request.GET.get('pot_radius', None)
        seed_radius = request.GET.get('seed_radius', None)

        # check to see if all parameters are met
        if pot_radius and seed_radius:
            try:
                pot_radius = float(pot_radius)
                seed_radius = float(seed_radius)
            except ValueError:
                return Response("Please enter numbers for pot_radius, and seed_radius")
        else:
            return Response("Please specify pot_radius, and seed_radius in your parameters")
        
        image_string = self.circular_pot(request).data['image']
        image = Image.open(cStringIO.StringIO(base64.b64decode(image_string)))
        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "JPEG")
        return response

    @list_route(methods=['get'])
    def rectangular_pot_image(self, request):
        """
        GET method implementation of calculating pot size

        Similar to rectangular_pot, but returns an image instead
        """
        pot_length = request.GET.get('pot_length', None)
        pot_width = request.GET.get('pot_width', None)
        seed_radius = request.GET.get('seed_radius', None)

        # check to see if all parameters are met
        if pot_length and pot_width and seed_radius:
            try:
                pot_length = float(pot_length)
                pot_width = float(pot_width)
                seed_radius = float(seed_radius)
            except ValueError:
                return Response("Please enter numbers for pot_length, pot_width, and seed_radius")
        else:
            return Response("Please specify pot_length, pot_width, and seed_radius in your parameters")
        
        # draw circles
        image_string = self.rectangular_pot(request).data['image']
        image = Image.open(cStringIO.StringIO(base64.b64decode(image_string)))
        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "JPEG")
        return response
