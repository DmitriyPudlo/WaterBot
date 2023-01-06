token_water = '747b8d86-2591-4aa2-bd3e-b8d2cbe3660d'
token_geo = '4153bafb-b6be-4097-814d-653ade3ffac5'
msg_text = 'Сейчас на улице {}°C, но ощущается как {}°C. Ветер {}, {}м/с, порывами до {}м/с.'
dict_wind_dir = {'nw': 'северо-западный',
                 'n': 'северный',
                 'ne': 'северо-восточный',
                 'e': 'восточный',
                 'se': 'юго-восточный',
                 's': 'южный',
                 'sw': 'юго-западный',
                 'w': 'западный',
                 'x': 'штиль'}


jsonsTEST = {'now': 1672998399, 'now_dt': '2023-01-06T09:46:39.209061Z',

         'info': {'url': 'https://yandex.ru/pogoda/48?lat=51.7727&lon=55.0988', 'lat': 51.7727, 'lon': 55.0988},

         'fact': {'obs_time': 1672995600, 'temp': -2, 'feels_like': -8, 'icon': 'ovc_-sn', 'condition': 'light-snow',
                  'wind_speed': 5, 'wind_dir': 's', 'pressure_mm': 742, 'pressure_pa': 989, 'humidity': 93,
                  'daytime': 'd', 'polar': False, 'season': 'winter', 'wind_gust': 10.8},
         'forecast': {'date': '2023-01-06', 'date_ts': 1672945200, 'week': 1, 'sunrise': '09:25', 'sunset': '17:24',
                      'moon_code': 0, 'moon_text': 'moon-code-0',
                      'parts': [{'part_name': 'evening', 'temp_min': -2, 'temp_avg': -1, 'temp_max': -1,
                                 'wind_speed': 6.3, 'wind_gust': 12.4, 'wind_dir': 's', 'pressure_mm': 739,
                                 'pressure_pa': 985, 'humidity': 95, 'prec_mm': 1.6, 'prec_prob': 80,
                                 'prec_period': 240, 'icon': 'ovc_+sn', 'condition': 'snow', 'feels_like': -8,
                                 'daytime': 'n', 'polar': False
                                 },
                                {'part_name': 'night', 'temp_min': -11, 'temp_avg': -5, 'temp_max': -1,
                                 'wind_speed': 5.7, 'wind_gust': 10.9, 'wind_dir': 'w', 'pressure_mm': 741,
                                 'pressure_pa': 987, 'humidity': 93, 'prec_mm': 0.9, 'prec_prob': 60,
                                 'prec_period': 480, 'icon': 'ovc_-sn', 'condition': 'light-snow',
                                 'feels_like': -12, 'daytime': 'n', 'polar': False
                                 }
                                ]
                      }
         }

coordinates = {'lat': 51.7727, 'lon': 55.0988}