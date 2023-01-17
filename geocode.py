import requests
from config import TOKEN_GEO
from city_list import city_list


class Geocode:
    def __init__(self):
        self.token_geo = TOKEN_GEO
        self.url = 'https://geocode-maps.yandex.ru/1.x'
        self.format = 'json'
        self.lang = 'ru_RU'

    def get_coordinates(self, city):
        if city not in city_list:
            return False
        params = {'geocode': city,
                  'apikey': self.token_geo,
                  'format': self.format,
                  'results': 1,
                  'lang': self.lang}
        response = requests.get(self.url, params=params)
        json = response.json()
        data = json['response']
        geoobjectcollection = data['GeoObjectCollection']
        featurmember = geoobjectcollection['featureMember'][0]
        geoobject = featurmember['GeoObject']
        point = geoobject['Point']
        pos = point['pos']
        coordinates = [float(point) for point in pos.split()]
        return {'lon': coordinates[0], 'lat': coordinates[1], 'lang': self.lang}
