import datetime

from terrarium.geomap.models import Place
from terrarium.geomap.models import PlacePolygon
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class PlacePolygonSerializer(serializers.ModelSerializer):
    """
    Serializer for PlacePolygon
    """
    last_updated = serializers.DateTimeField(default=datetime.datetime.now())
    class Meta:
        model = PlacePolygon
        fields = ('last_updated', 'polygon', 'place')
        extra_kwargs = {'place': {'write_only': True,
                                  'required': False}}

    def create(self, validated_data):
        """
        Create and return a new ``PlacePolygon`` instance, given the validated
        data.
        """
        return PlacePolygon.objects.create(**validated_data)

class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for Place
    """
    polygons = PlacePolygonSerializer(many=True)
    class Meta:
        model = Place
        fields = ('display_name', 'osm_id', 'osm_type', 'last_updated',
                  'place_id', 'polygons')

    def create(self, validated_data):
        """
        Create and return a new ``Place`` instance, given the validated data.
        """

        # remove polygon information and let PlacePolyonSerializer deal with it
        if 'polygons' in validated_data and len(validated_data['polygons']):
            polygon_data = validated_data.pop('polygons')
        else:
            raise ValidationError('Please provide a valid GeoJSON representation')

        place = Place.objects.create(**validated_data)
        
        if polygon_data:
            for shape in polygon_data:
                shape['place'] = place.id
                polygon_serializer = PlacePolygonSerializer(data=shape)
                if polygon_serializer.is_valid():
                    polygon = polygon_serializer.save()

        return place

