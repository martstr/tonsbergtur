
from rest_framework import serializers

class CoordinateSerializer(serializers.Serializer):
    # TODO: Oppdater med relevant oppgave
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()