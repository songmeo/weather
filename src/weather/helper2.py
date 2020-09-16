import json, datetime
import requests, os

APIKEY = os.environ['API_KEY']
API_URL = 'https://api.climacell.co/v3/weather/historical/station'

querystring = {
    'apikey': APIKEY,
    'start_time': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
    'end_time': datetime.datetime.now(),
}

def get_parameter_value(para):
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
        v['value'] = p[para['name']]['value']
        values.append(v)
    para = Parameter(
        name=para['name'],
        values=values,
        unit=data[0][para['name']]['units']
    )
    para.save()
    return para

def get_values(para):
    data = get_parameter_value(para)
    values = []
    for p in data:
        v = {}
        v['observation_time'] = p['observation_time']['value']
        v['value'] = p[para.name]['value']
        values.append(v)
    unit = data[0][para.name]['units']
    return unit, values
