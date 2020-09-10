from rest_framework import serializers
from .models import City, Parameter
from .helper import add_city

class CitySerializer(serializers.ModelSerializer):
    parameters = serializers.HyperlinkedRelatedField(read_only=True, view_name='Parameters')
    class Meta:
        model = City
        fields = '__all__'
    def to_representation(self, obj):
        return add_city(self, obj)

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name', 'location', 'unit', 'avg', 'min', 'max')