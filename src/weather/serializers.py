from rest_framework import serializers
from .models import City, Parameter
from .helper import add_city

class CitySerializer(serializers.ModelSerializer):
    #parameters = serializers.HyperlinkedRelatedField(read_only=True, view_name='location-parameters-list', many=True)
    class Meta:
        model = City
        fields = ('id', 'name', 'description', 'longitude', 'latitude')
    def create(self, validated_data):
        return add_city(validated_data)

class ParameterSerializer(serializers.ModelSerializer):
    #location = serializers.HyperlinkedRelatedField(read_only=True, view_name='city-detail')
    avg = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    max = serializers.SerializerMethodField()
    def get_avg(self, obj):
        values = [d['value'] for d in obj.values if d['value'] is not None]
        if len(values) == 0:
            return None
        return sum(values) / len(values)
    def get_min(self, obj):
        values = [d['value'] for d in obj.values if d['value'] is not None]
        return min(values, default=None)
    def get_max(self, obj):
        values = [d['value'] for d in obj.values if d['value'] is not None]
        return max(values, default=None)
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'unit', 'avg', 'min', 'max', 'values')