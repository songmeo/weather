from django.db import models
from django.http import HttpRequest

class City(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=64, blank=True)
    parameters = models.URLField(max_length=200, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'cities'

#e.g temperature, humidity
class Parameter(models.Model):
    name = models.CharField(max_length=25)
    location = models.URLField(max_length=200, blank=True)
    unit = models.CharField(max_length=10)
    values = models.JSONField
    def __str__(self):
        return self.name