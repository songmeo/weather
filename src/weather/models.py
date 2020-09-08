from django.db import models
from django.http import HttpRequest
from .helper import get_data
from django.http import HttpRequest

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=64, blank=True)
    parameters = models.URLField(max_length=200, blank=True)
    class Meta:
        verbose_name_plural = 'cities'
    def __str__(self):
        return self.name
    def aggregation(self):
        return get_data(self.name)

#e.g temperature, humidity
class Parameter(models.Model):
    name = models.CharField(max_length=25)
    location = models.URLField(max_length=200, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    values = models.JSONField(default=dict)
    avg = models.FloatField(null=True)
    min = models.FloatField(null=True)
    max = models.FloatField(null=True)
    _city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


