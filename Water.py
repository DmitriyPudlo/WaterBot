import requests
from Coordinates import Coordinates
from Config import token_water


class Water:
    def __init__(self):
        self.url = 'https://api.weather.yandex.ru/v2/informers/'
        self.lang = 'ru_RU'
        self.token_water = token_water
        self.coordinates = Coordinates().Check_coordinates()

    def Check_weather(self):
        params = {'lat': self.coordinates['lat'],
                  'lon': self.coordinates['lon'],
                  'lang': self.lang}
        headers = {'X-Yandex-API-Key': self.token_water}
        water_response = requests.get(self.url, params=params, headers=headers)
        water_json = water_response.json()
        return water_json
