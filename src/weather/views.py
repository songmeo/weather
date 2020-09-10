from .models import City, Parameter
from rest_framework import viewsets
from .serializers import CitySerializer, ParameterSerializer
from rest_framework.decorators import action
from .helper import add_city

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    @action(detail=False, methods=['get'])
    def test(self, request):
        return Response(self.get_serializer(many=True))
    
class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer