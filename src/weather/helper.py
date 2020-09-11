import json, datetime
import requests
from .models import City, Parameter
from config.secret import apikey

API_URL = 'https://api.climacell.co/v3/weather/historical/station'
FIELDS = "temp,precipitation,feels_like,dewpoint,wind_speed,wind_gust,baro_pressure,visibility,humidity,wind_direction,cloud_cover,cloud_ceiling,cloud_base"
querystring = {
    'apikey': apikey,
    'start_time': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
    'end_time': datetime.datetime.now(),
    'fields': FIELDS
}

def take_parameters_data(city):
    querystring['lat'] = city.latitude
    querystring['lon'] = city.longitude
    response = requests.get(API_URL, params=querystring)
    return response

def add_city(obj):
    with open('weather/static/cities.json') as fd:
        cities = json.load(fd)
    city_location = [c for c in cities if(c['name'] == obj['name'])][0]
    city = City(
        name=city_location['name'],
        description=obj['description'],
        longitude=float(city_location['lng']),
        latitude=float(city_location['lat'])
    )
    city.save()
    parameters_data = take_parameters_data(city).json()
    print(parameters_data)
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
            _city=city
        )
        parameter.save()
    return city
