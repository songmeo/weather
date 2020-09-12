from rest_framework import serializers
from .models import Location, Parameter
from .helper import add_location, aggregate

class AggregationField(serializers.RelatedField):
    def to_representation(self, value):
        avg, min_val, max_val = aggregate(value)
        return {
            'id': value.id,
            'name': value.name,
            'avg': avg,
            'min': min_val,
            'max': max_val,
            'units': value.unit
        }

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'values')
    def to_representation(self, value):
        avg, min_val, max_val = aggregate(value)
        return {
            'id': value.id,
            'name': value.name,
            'avg': avg,
            'min': min_val,
            'max': max_val,
            'units': value.unit,
            'values': value.values
        }

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    parameters = serializers.HyperlinkedIdentityField(view_name='weather:location-parameters-list', lookup_url_kwarg='location_pk')
    aggregation = AggregationField(many=True, read_only=True, source="parameters")
    class Meta:
        model = Location
        fields = ('id', 'name', 'description','longitude', 'latitude', 'parameters', 'aggregation')
    def create(self, validated_data):
        return add_location(validated_data)

