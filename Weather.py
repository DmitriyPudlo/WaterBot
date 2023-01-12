import requests
from Config import TOKEN_WATER
from Messages import msg_text, dict_wind_dir, dict_condition, times_of_day


class Weather:
    def __init__(self):
        self.url = 'https://api.weather.yandex.ru/v2/informers/'
        self.token_water = TOKEN_WATER

    def check_weather(self, coordinates):
        headers = {'X-Yandex-API-Key': self.token_water}
        weather_response = requests.get(self.url, params=coordinates, headers=headers)
        weather_json = weather_response.json()
        to_bot = self.__prepare_info(weather_json)
        return to_bot

    def __prepare_info(self, weather_json):
        fact_weather = weather_json['fact']
        fact_temp = fact_weather['temp']
        feels_like = fact_weather['feels_like']
        wind_speed = fact_weather['wind_speed']
        wind_dir = fact_weather['wind_dir']
        wind_gust = fact_weather['wind_gust']
        condition = fact_weather['condition']
        forecast = weather_json['forecast']
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
