from django.urls import path, include
from .views import CityViewSet, ParameterViewSet
from rest_framework_nested import routers

app_name = "weather"

router = routers.DefaultRouter()
router.register(r'locations', CityViewSet)

locations_router = routers.NestedDefaultRouter(router, r'locations', lookup='location')
locations_router.register(r'parameters', ParameterViewSet, basename='location-parameters')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(locations_router.urls))
]