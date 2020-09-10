import json, datetime
import requests
from .models import City
from config.secret import apikey

API_URL = 'https://api.climacell.co/v3/insights/fire-index'
querystring = {
    'apikey': apikey,
    'start_time': datetime.datetime.now() - datetime.timedelta(days=1),
    'end_time': 'now',
    'fields': "temp, precipitation, feels_like, dewpoint, wind_speed, wind_gust, baro_pressure, visibility, humidity, wind_direction, sunrise, sunset, cloud_cover, cloud_ceiling, cloud_base, surface_shortwave_radiation"
}

def add_parameters(obj):
    querystring['lat'] = obj['latitude']
    querystring['lon'] = obj['longitude']
    response = requests.request("GET", API_URL, params=querystring)
    print(response)

def add_city(obj):
    with open('weather/static/cities.json') as fd:
        cities = json.load(fd)
    city_location = [c for c in cities if(c['name'] == obj['name'])][0]
    print(city_location)
    city = City(
        name=city_location['name'],
        description=obj['description'],
        longitude=float(city_location['lng']),
        latitude=float(city_location['lat'])
    )
    #add parameters
    add_parameters(city)
    city.save()
    return city
