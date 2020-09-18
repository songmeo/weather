from .models import Location, Parameter
from rest_framework import viewsets
from .serializers import LocationSerializer, ParameterSerializer, ErrorSerializer
from .helper import update_parameter, add_parameter
from rest_framework.response import Response
from django.db import IntegrityError

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    def get_queryset(self):
        locations = Location.objects.all()
        for loc in locations:
            for para in loc.parameters.all():
                try:
                    update_parameter(para)
                except RuntimeError as err:
                    serializer = ErrorSerializer(err).data
                    return serializer
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

    def create(self, request, location_pk):
        loc = Location.objects.filter(id=location_pk)[0]
        try:
            para = add_parameter(loc, request.data['name'])
            data = ParameterSerializer(para).data
        except (RuntimeError, IntegrityError) as err:
            data = ErrorSerializer(err).data
        return Response(data)
        