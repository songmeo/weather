from rest_framework import serializers
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=64, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    class Meta:
        verbose_name_plural = 'cities'
    def __str__(self):
        return self.name
        
#e.g temperature, humidity
class Parameter(models.Model):
    name = models.CharField(max_length=25)
    unit = models.CharField(max_length=10, blank=True)
    values = models.JSONField(default=list)
    _city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="parameters")
    def __str__(self):
        return self.name


