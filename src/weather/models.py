from rest_framework import serializers
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    class Meta:
        verbose_name_plural = 'locations'
    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=25)
    unit = models.CharField(max_length=10, blank=True)
    values = models.JSONField(default=list, blank=True, null=True)
    _location = models.ForeignKey(Location, 
                                on_delete=models.CASCADE, 
                                related_name="parameters"
                )
    class Meta:
        unique_together = (('name','_location'))
    def __str__(self):
        return self.name
