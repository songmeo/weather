import requests
from .models import City
API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=84476c2c5b591ae9b18a513cab190ef8'

def query(location):
    url = API_URL.format(location)
    result = requests.get(url)
    return result.json()

def add_city(self, obj):
    data = query(obj.name)
    if data["cod"] == "200":
        #check if city is in list
        city_data = data["city"]
        try:
            city = City.objects.get(name=city_data["name"])
        except city.DoesNotExist:
            city = City(
                ref=city_data["id"],
                name=city_data["name"],
                location_id=city_data["country"],
                parameters=f"http://{self.context['request'].get_host()}/locations/{obj.id}/parameters",
            )
            city.save()
            return city
'''
def serialize_city(self, obj):
    return {
        'ref': 
    }
'''

'''
def add_parameter(self, obj):
    data = query(obj.name)
    if data["cod"] == "200":
        #check if city is in list
        city_data = data["city"]
        try:
            city = City.objects.get(ref=city_data["id"])
        except city.DoesNotExist:
            city = City(
                ref=city_data["id"],
                name=city_data["name"],
                location_id=city_data["country"],
                parameters=f"http://{self.context['request'].get_host()}/locations/{obj.id}/parameters",
            )
            city.save()
        return city.aggregation
'''
