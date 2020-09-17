from .models import Location, Parameter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from .serializers import LocationSerializer, ParameterSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView 
from .helper import get_parameter_values

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Parameter.objects.filter(_location=self.kwargs['location_pk'])
    serializer_class = ParameterSerializer

    def get_serializer_context(self):
        context = super(ParameterViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context