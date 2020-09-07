from rest_framework import serializers
from .models import City, Parameter
from .helper import get_data

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('__all__', 'avg', 'min', 'max')