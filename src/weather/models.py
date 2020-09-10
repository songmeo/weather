from rest_framework import serializers
from django.db import models

class City(models.Model):
    #ref = models.IntegerField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=64, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    #aggregation = models.JSONField(default=dict, blank=True)
    class Meta:
        verbose_name_plural = 'cities'
    def __str__(self):
        return self.name
        
#e.g temperature, humidity
class Parameter(models.Model):
    name = models.CharField(max_length=25)
    #location = models.URLField(max_length=200, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    #values = models.JSONField(default=dict)
    avg = models.FloatField(null=True)
    min = models.FloatField(null=True)
    max = models.FloatField(null=True)
    _city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


