import json, datetime
import requests, os
from .models import Location, Parameter
#from .serializers import ParameterSerializer
#from config.secret import apikey

APIKEY = os.environ['API_KEY']
API_URL = 'https://api.climacell.co/v3/weather/historical/station'
#feels_like,dewpoint,wind_speed,wind_gust,baro_pressure,wind_direction,cloud_cover,cloud_ceiling,cloud_base,visibility
FIELDS = "temp,precipitation,humidity"
querystring = {
    'apikey': APIKEY,
    'start_time': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
    'end_time': datetime.datetime.now(),
}
with open('weather/static/cities.json') as fd:
    CITIES = json.load(fd)

# get parameter data from climacell
def get_parameter_values(location):
    querystring['lat'] = location.latitude
    querystring['lon'] = location.longitude
    parameters = location.parameters.all()
    fields = ','.join([para.name for para in parameters])
    querystring['fields'] = fields
    data = requests.get(API_URL, params=querystring).json()
    for f in fields.split(','):
        values = []
        for p in data:
            values = []
        for p in data:
            v = {}
            v['observation_time'] = p['observation_time']['value']
            v['value'] = p[f]['value']
            values.append(v)
    return values

def add_location(obj):
    loc = [c for c in CITIES if(c['name'] == obj['name'])][0]
    location = Location(
        name=loc['name'],
        description=obj['description'],
        longitude=float(loc['lng']),
        latitude=float(loc['lat'])
    )
    location.save()

    #add parameters
    fields = "temp,precipitation,humidity"
    for f in fields.split(','):
        para = Parameter(
            name=f,
            _location=location
        )
        add_parameter(para)
    return location

def get_parameter_value(para):
    print(para)
    querystring['lat'] = para._location.latitude
    querystring['lon'] = para._location.longitude
    querystring['fields'] = para.name
    data = requests.get(API_URL, params=querystring).json()
    return data

def add_parameter(para):
    data = get_parameter_value(para)
    values = []
    for p in data:
        v = {}
        v['observation_time'] = p['observation_time']['value']
        v['value'] = p[para.name]['value']
        values.append(v)
    para = Parameter(
        name=para.name,
        values=values,
        unit=data[0][para.name]['units'],
        _location=para._location
    )
    para.save()
    return para


def aggregate(value):
    values = [d['value'] for d in value if d['value'] is not None]
    data = {
        'min': min(values, default=None),
        'max': max(values, default=None),
        'avg': round(sum(values) / len(values), 2) if values else None 
    }
    return data
