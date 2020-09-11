from rest_framework import serializers
from .models import City, Parameter
from .helper import add_city, aggregate

class CityAggregationField(serializers.RelatedField):
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
    #location = serializers.HyperlinkedRelatedField(read_only=True, view_name='city-detail')
    #aggregation = ParameterAggregationField(many=True, read_only=True, source="values")
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

class CitySerializer(serializers.ModelSerializer):
    #parameters = serializers.HyperlinkedRelatedField(read_only=True, lookup_field='id', view_name='location-parameters-list', many=True)
    aggregation = CityAggregationField(many=True, read_only=True, source="parameters")
    class Meta:
        model = City
        fields = ('id', 'name', 'description', 'longitude', 'latitude', 'aggregation')
    def create(self, validated_data):
        return add_city(validated_data)

