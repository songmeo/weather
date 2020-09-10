from rest_framework import serializers
from .models import City, Parameter
from .helper import add_city

class CitySerializer(serializers.ModelSerializer):
    parameters = serializers.HyperlinkedRelatedField(read_only=True, view_name='location-parameters-list')
    class Meta:
        model = City
        fields = ('id', 'name', 'description', 'longitude', 'latitude', 'parameters')
    def create(self, validated_data):
        return add_city(validated_data)

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name', 'location', 'unit', 'avg', 'min', 'max')