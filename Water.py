import requests
from Config import token_water, msg_text, dict_wind_dir, jsonsTEST, coordinates


class Water:
    def __init__(self):
        self.url = 'https://api.weather.yandex.ru/v2/informers/'
        self.lang = 'ru_RU'
        self.token_water = token_water

    def check_weather(self, coordinates):
        params = {'lat': coordinates['lat'],
                  'lon': coordinates['lon'],
                  'lang': self.lang}
        headers = {'X-Yandex-API-Key': self.token_water}
        water_response = requests.get(self.url, params=params, headers=headers)
        water_json = water_response.json()
        # water_json = jsonsTEST
        to_bot = self.__prepare_info(water_json)
        return to_bot

    def __prepare_info(self, water_json):
        fact_water = water_json['fact']
        fact_temp = fact_water['temp']
        feels_like = fact_water['feels_like']
        wind_speed = fact_water['wind_speed']
        wind_dir = fact_water['wind_dir']
        wind_gust = fact_water['wind_gust']
        to_bot = msg_text.format(fact_temp, feels_like, dict_wind_dir[wind_dir], wind_speed,  wind_gust)
        return to_bot
