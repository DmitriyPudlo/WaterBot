import requests
from Config import token_geo


class Coordinates:
    def __init__(self):
        self.token_geo = token_geo
        self.url = 'https://geocode-maps.yandex.ru/1.x'
        self.format = 'json'
        self.lang = 'ru_RU'

    def check_coordinates(self, city):
        params = {'geocode': city,
                  'apikey': self.token_geo,
                  'format': self.format,
                  'results': 1,
                  'lang': self.lang}
        coordinates_response = requests.get(self.url, params=params)
        coordinates_json = coordinates_response.json()
        coordinates_data = coordinates_json['response']
        coordinates_geoobjectcollection = coordinates_data['GeoObjectCollection']
        coordinates_featurmember = coordinates_geoobjectcollection['featureMember'][0]
        coordinates_geoobject = coordinates_featurmember['GeoObject']
        coordinates_point = coordinates_geoobject['Point']
        coordinates_pos = coordinates_point['pos']
        coordinates = [float(point) for point in coordinates_pos.split()]
        return {'lat': coordinates[1], 'lon': coordinates[0]}
