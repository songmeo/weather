from rest_framework import serializers
from .models import Location, Parameter
from .helper import add_location, aggregate, get_parameter_values, add_parameter

class ParameterSerializer(serializers.ModelSerializer):
    aggregation = serializers.SerializerMethodField()
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'aggregation', 'values')
    def get_aggregation(self, obj):
        return aggregate(obj.values)
    def create(self, obj):
        return add_parameter(obj)

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    parameters = serializers.HyperlinkedIdentityField(view_name='weather:location-parameters-list', lookup_url_kwarg='location_pk')
    aggregation = serializers.JSONField(default=dict, source="parameters.aggregation")
    class Meta:
        model = Location
        fields = ('id', 'name', 'description','longitude', 'latitude', 'aggregation', 'parameters')
    def create(self, obj):
        return add_location(obj)

