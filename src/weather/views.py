from .models import City, Parameter
from rest_framework import viewsets
from .serializers import CitySerializer, ParameterSerializer
from rest_framework.decorators import action

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer