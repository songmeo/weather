from .models import City
from rest_framework import viewsets
from .serializers import CitySerializer

# Create your views here.
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

