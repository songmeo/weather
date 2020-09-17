from .models import Location, Parameter
from rest_framework import viewsets
from .serializers import LocationSerializer, ParameterSerializer
from .helper import update_parameter

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    def get_queryset(self):
        locations = Location.objects.all()
        for loc in locations:
            for para in loc.parameters.all():
                update_parameter(para)
        return locations
    serializer_class = LocationSerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        paras = Parameter.objects.filter(_location=self.kwargs['location_pk'])
        for para in paras:
            update_parameter(para)
        return paras
    serializer_class = ParameterSerializer

    def get_serializer_context(self):
        context = super(ParameterViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
