import requests
from Config import TOKEN_GEO


class Geocode:
    def __init__(self):
        self.token_geo = TOKEN_GEO
        self.url = 'https://geocode-maps.yandex.ru/1.x'
        self.format = 'json'
        self.lang = 'ru_RU'

    def check_coordinates(self, city):
        params = {'geocode': city,
                  'apikey': self.token_geo,
                  'format': self.format,
                  'results': 1,
                  'lang': self.lang}
        response = requests.get(self.url, params=params)
        json = response.json()
        data = json['response']
        geoobjectcollection = data['GeoObjectCollection']
        if len(geoobjectcollection['featureMember']) == 0:
            return False
        featurmember = geoobjectcollection['featureMember'][0]
        geoobject = featurmember['GeoObject']
        point = geoobject['Point']
        pos = point['pos']
        coordinates = [float(point) for point in pos.split()]
        return {'lon': coordinates[0], 'lat': coordinates[1], 'lang': self.lang}
