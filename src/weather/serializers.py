from rest_framework import serializers
from .models import Location, Parameter
from django.http import HttpRequest
from django.urls import reverse, resolve
from .helper import add_location, aggregate, get_parameter_values, add_parameter

class ParameterSerializer(serializers.ModelSerializer):
    aggregation = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'location', 'aggregation', 'values')
    
    def get_aggregation(self, obj):
        return aggregate(obj.values)
    def get_location(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('weather:location-detail', args=[obj._location.id]))
    def create(self, obj):
        return add_parameter(obj._location, obj.name)

class AggregationField(serializers.RelatedField):
    def to_representation(self, obj):
        aggregation = aggregate(obj.values)
        if 'message' in aggregation:
            return {
                'id': obj.id,
                'name': obj.name,
                'message': aggregation['message']
            }
        return {
            'id': obj.id,
            'name': obj.name,
            'min': aggregation['min'],
            'max': aggregation['max'],
            'avg': aggregation['avg']
        }
class LocationSerializer(serializers.ModelSerializer):
    parameters = serializers.HyperlinkedIdentityField(view_name='weather:location-parameters-list', lookup_url_kwarg='location_pk')
    aggregation = AggregationField(many=True,source="parameters",read_only=True)
    class Meta:
        model = Location
        fields = ('id','name', 'description','longitude', 'latitude', 'parameters', 'aggregation')
    def get_aggregation(self, obj):
        aggregations = []
        paras = obj.parameters.all()
        for p in paras:
            aggregations.append(aggregate(p.values))
        return aggregations
    def create(self, obj):
        return add_location(obj)
