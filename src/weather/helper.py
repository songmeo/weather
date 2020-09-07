import requests
API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=84476c2c5b591ae9b18a513cab190ef8'

def get_data(city):
    r = requests.get(API_URL.format(city)).json()
    data = {
        'temperature': r['list'][0]['main']['temp']
    }
    return data