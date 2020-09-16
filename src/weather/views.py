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
'''
@api_view(['GET', 'POST'])
def location_list(request):
    if(m)
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def location_detail(request, pk):
    try:
        loc = Location.objects.get(pk=pk)
    except loc.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = LocationSerializer(loc)
    return Response(serializer.data)
class LocationView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    def post(self, request):
        return self.create(request)
'''

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
class ParameterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Parameter.objects.filter(_location=self.kwargs['location_pk'])
    serializer_class = ParameterSerializer