from rest_framework import serializers
from .models import Location, Parameter
from django.http import HttpRequest
from django.urls import reverse, resolve
#from django.core.urlresolvers import reverse
from .helper import add_location, aggregate, get_parameter_values, add_parameter

class ParameterSerializer(serializers.ModelSerializer):
    aggregation = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'aggregation', 'location', 'values')
    
    def get_aggregation(self, obj):
        return aggregate(obj.values)
    def get_location(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('weather:location-detail', args=[obj._location.id]))
    def create(self, obj):
        return add_parameter(obj)

class LocationSerializer(serializers.ModelSerializer):
    parameters = serializers.HyperlinkedIdentityField(view_name='weather:location-parameters-list', lookup_url_kwarg='location_pk')
    aggregation = serializers.JSONField(default=dict, source="parameters.aggregation", allow_null=True)
    class Meta:
        model = Location
        fields = ('id','name', 'description','longitude', 'latitude', 'aggregation', 'parameters')
    def create(self, obj):
        return add_location(obj)