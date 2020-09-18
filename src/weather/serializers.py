from rest_framework import serializers
from .models import Location, Parameter
from collections import OrderedDict
from django.http import HttpRequest
from django.urls import reverse, resolve
from .helper import add_location, aggregate, add_parameter, serialize_error

class ParameterSerializer(serializers.ModelSerializer):
    aggregation = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'location', 'aggregation', 'message', 'values')
    def get_message(self, obj):
        if not obj.values:
            return "no data available for this parameter."
        return None
    def get_aggregation(self, obj):
        return aggregate(obj.values)
    def get_location(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('weather:location-detail', args=[obj._location.id]))
    def to_representation(self, obj):
        result = super(ParameterSerializer, self).to_representation(obj)
        return OrderedDict([(key, result[key]) for key in result if result[key]])

class ErrorSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return serialize_error(str(obj))

class AggregationField(serializers.RelatedField):

    def to_representation(self, obj):
        aggregation = aggregate(obj.values)
        if aggregation:
            return {
                'id': obj.id,
                'name': obj.name,
                'min': aggregation['min'],
                'max': aggregation['max'],
                'avg': aggregation['avg']
            }
        return {
            'id': obj.id,
            'name': obj.name,
            'message': 'no data available for this parameter.'
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
    def to_representation(self, obj):
        result = super(LocationSerializer, self).to_representation(obj)
        return OrderedDict([(key, result[key]) for key in result if result[key]])
