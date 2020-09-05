from django.urls import path, include
from .views import CityViewSet
from rest_framework.routers import DefaultRouter

app_name = "weather"

router = DefaultRouter()
router.register('locations', CityViewSet, basename='locations')
urlpatterns = [
    path("", include(router.urls)),
]