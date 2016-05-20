from terrarium.plants.models import Plant
from rest_framework import serializers

class PlantSerializer(serializers.ModelSerializer):
    """
    Serializer for Plant
    """
    class Meta:
        model = Plant
