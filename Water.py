import requests
from Config import token_water, msg_text, dict_wind_dir, dict_condition, times_of_day


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
        condition = fact_water['condition']
        forecast = water_json['forecast']
        parts = forecast['parts']
        part_one = parts[0]
        part_two = parts[1]
        part_name_one = part_one['part_name']
        part_name_two = part_two['part_name']
        forecast_temp_avg_one = part_one['temp_avg']
        forecast_wind_speed_one = part_one['wind_speed']
        forecast_wind_dir_one = part_one['wind_dir']
        forecast_wind_gust_one = part_one['wind_gust']
        forecast_condition_one = part_one['condition']
        forecast_temp_avg_two = part_two['temp_avg']
        forecast_wind_speed_two = part_two['wind_speed']
        forecast_wind_dir_two = part_two['wind_dir']
        forecast_wind_gust_two = part_two['wind_gust']
        forecast_condition_two = part_two['condition']
        to_bot = msg_text.format(fact_temp, feels_like, dict_wind_dir[wind_dir], wind_speed,  wind_gust, dict_condition[condition],
                                 times_of_day[part_name_one], forecast_temp_avg_one, dict_wind_dir[forecast_wind_dir_one], forecast_wind_speed_one, forecast_wind_gust_one, dict_condition[forecast_condition_one],
                                 times_of_day[part_name_two], forecast_temp_avg_two, dict_wind_dir[forecast_wind_dir_two], forecast_wind_speed_two, forecast_wind_gust_two, dict_condition[forecast_condition_two])
        return to_bot
