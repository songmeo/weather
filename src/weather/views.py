from .models import Location, Parameter
from rest_framework import viewsets
from .serializers import LocationSerializer, ParameterSerializer
from rest_framework.decorators import action

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Parameter.objects.filter(_location=self.kwargs['location_pk'])
    serializer_class = ParameterSerializer