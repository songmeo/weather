from .models import Location, Parameter
from rest_framework import viewsets
from .serializers import LocationSerializer, ParameterSerializer
from .helper import get_parameter_values

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        paras = Parameter.objects.filter(_location=self.kwargs['location_pk'])
        return paras
    serializer_class = ParameterSerializer

    def get_serializer_context(self):
        context = super(ParameterViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
