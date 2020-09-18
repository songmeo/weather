import json, datetime, dateutil.parser
import requests, os
from django.http import Http404
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

def add_location(loc):
    try:
        location = [c for c in CITIES if(c['name'] == loc['name'])][0]
    except:
        raise Http404("City not found")
    location = Location.objects.create(name=loc['name'],
                                       description=loc['description'],
                                       longitude=float(location['lng']),
                                       latitude=float(location['lat'])
                                      )
    fields = "temp,precipitation,humidity"
    for field in fields.split(','):
        add_parameter(location, field)
    return location

# get parameter data from climacell
def get_parameter_value(lat, lng, field):
    querystring['lat'] = lat
    querystring['lon'] = lng
    querystring['fields'] = field
    response = requests.get(API_URL, params=querystring)
    if response.status_code == 400:
        raise RuntimeError("This parameter is not supported. Supported parameters are temp,precipitation,humidity,\
                            feels_like,dewpoint,wind_speed,wind_gust,baro_pressure,wind_direction, \
                            cloud_cover,cloud_ceiling,cloud_base,visibility,temp,precipitation,humidity")
    elif response.status_code == 429:
        raise RuntimeError("API calls exceeded")
    data = response.json()
    values = []
    for p in data:
        v = {}
        if p[field]['value'] is None:
            continue
        v['value'] = p[field]['value']
        v['observation_time'] = p['observation_time']['value']
        values.append(v)
    unit = data[0][field]['units']
    return values, unit

def add_parameter(location_obj, field):
    values, unit = get_parameter_value(location_obj.latitude, location_obj.longitude, field)
    para = Parameter.objects.create(_location=location_obj,
                                    values=values,
                                    name=field,
                                    unit=unit
                                    )
    return para

def aggregate(value):
    values = [d['value'] for d in value if d['value'] is not None]
    if not values:
        return None
    return {
        'min': min(values, default=None),
        'max': max(values, default=None),
        'avg': round(sum(values) / len(values), 2) if values else None 
    }

def update_parameter(para):
    values = para.values
    if values:
        last_update_time = values[-1]['observation_time']
        now = datetime.datetime.now(datetime.timezone.utc)
        interval = now - dateutil.parser.isoparse(last_update_time)
        if interval < datetime.timedelta(hours=6):
            return
    loc = para._location
    field = para.name
    try:
        values = get_parameter_value(loc.latitude, loc.longitude, field)[0]
        para.values = values
    except RuntimeError:
        para.values = []
    para.save()

def serialize_error(message):
    return {
        'message': str(message)
    }