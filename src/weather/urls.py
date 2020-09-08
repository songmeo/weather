from django.urls import path, include
from .views import CityViewSet, ParameterViewSet
from rest_framework.routers import DefaultRouter

app_name = "weather"

router = DefaultRouter()
router.register('locations', CityViewSet)
router.register('parameters', ParameterViewSet)
urlpatterns = [
    path("", include(router.urls)),
]