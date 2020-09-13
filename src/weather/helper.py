import json, datetime
import requests, os
from .models import Location, Parameter
#from config.secret import apikey

APIKEY = os.environ['API_KEY']
API_URL = 'https://api.climacell.co/v3/weather/historical/station'
FIELDS = "temp,precipitation,feels_like,dewpoint,wind_speed,wind_gust,baro_pressure,visibility,humidity,wind_direction,cloud_cover,cloud_ceiling,cloud_base"
querystring = {
    'apikey': APIKEY,
    'start_time': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
    'end_time': datetime.datetime.now(),
    'fields': FIELDS
}

def take_parameters_data(location):
    querystring['lat'] = location.latitude
    querystring['lon'] = location.longitude
    response = requests.get(API_URL, params=querystring)
    return response

def add_parameters(location):
    parameters_data = take_parameters_data(location).json()
    for f in FIELDS.split(','):
        vals = []
        for p in parameters_data:
            v = {}
            v['observation_time'] = p['observation_time']['value']
            v['value'] = p[f]['value']
            vals.append(v)
        parameter = Parameter(
            name=f,
            unit=parameters_data[0][f]['units'],
            values=vals,
            _location=location
        )
        parameter.save()
    
def add_location(obj):
    with open('static/cities.json') as fd:
        cities = json.load(fd)
    loc = [c for c in cities if(c['name'] == obj['name'])][0]
    location = Location(
        name=loc['name'],
        description=obj['description'],
        longitude=float(loc['lng']),
        latitude=float(loc['lat'])
    )
    location.save()
    add_parameters(location)
    return location

def aggregate(value):
    values = [d['value'] for d in value.values if d['value'] is not None]
    if len(values) == 0:
        avg = None
    else:
        avg = round(sum(values) / len(values), 2)
    return avg, min(values, default=None), max(values, default=None)
