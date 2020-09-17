import json, datetime
import requests, os
from .models import Location, Parameter

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

def add_location(loc):
    location = [c for c in CITIES if(c['name'] == loc['name'])][0]
    location = Location.objects.create(name=loc['name'],
                                        description=loc['description'],
                                        longitude=float(location['lng']),
                                        latitude=float(location['lat'])
                                    )
    fields = "temp,precipitation,humidity"
    for field in fields.split(','):
        add_parameter(location, field)
    return location

def get_parameter_value(lat, lng, field):
    querystring['lat'] = lat
    querystring['lon'] = lng
    querystring['fields'] = field
    data = requests.get(API_URL, params=querystring).json()
    return data

def add_parameter(location_obj, field):
    data = get_parameter_value(location_obj.latitude, location_obj.longitude, field)
    values = []
    for p in data:
        v = {}
        v['observation_time'] = p['observation_time']['value']
        v['value'] = p[field]['value']
        values.append(v)
    para = Parameter.objects.create(_location=location_obj,
                                    values=values,
                                    name=field,
                                    unit=data[0][field]['units']
                                    )
    return para

def aggregate(value):
    values = [d['value'] for d in value if d['value'] is not None]
    data = {
        'min': min(values, default=None),
        'max': max(values, default=None),
        'avg': round(sum(values) / len(values), 2) if values else None 
    }
    return data
