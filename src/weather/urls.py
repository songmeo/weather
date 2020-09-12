from django.urls import path, include
from .views import LocationViewSet, ParameterViewSet
from rest_framework_nested import routers

app_name = "weather"

router = routers.SimpleRouter()
router.register('locations', LocationViewSet)

locations_router = routers.NestedSimpleRouter(router, 'locations', lookup='location')
locations_router.register('parameters', ParameterViewSet, basename='location-parameters')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(locations_router.urls))
]