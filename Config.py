import pass_token

TOKEN_WATER = f'{pass_token.TELEGRAM_TOKEN}'
TOKEN_GEO = f'{pass_token.TOKEN_GEO}'
TELEGRAM_TOKEN = f'{pass_token.TELEGRAM_TOKEN}'
DATABASE = f'{pass_token.DATABASE}'
USER = f'{pass_token.USER}'
PASSWORD = f'{pass_token.PASSWORD}'

msg_text = '''Сейчас на улице {}°C, но ощущается как {}°C. Ветер {}, {}м/с, порывами до {}м/с. {}. 
{} ожидается T воздуха {}°C. Ветер {}, {}м/с, порывами до {}м/с. {}. 
{} ожидается T воздуха {}°C. Ветер {}, {}м/с, порывами до {}м/с. {}.'''

msg_hello = 'Привет! Я твой помощник, который будет каждый день сообщать актуальную погоду на улице и ближайший ' \
            'прогноз. Тебе всего-лишь нужно указать город и время, в которое нужно присылать сообщение. '

msg_city = 'Напиши город!'

msg_time = 'Напиши время, в которое будет приходить сообщение, в формате "12:12"'

msg_complete = 'Замечательно! Жди прогноз в назначенное время!'

city_not_found = 'Город не найден'

time_error = 'Укажи время в правильном формате'

msg_bye = 'Работа бота остановлена. Пока!'

dict_wind_dir = {'nw': 'северо-западный',
                 'n': 'северный',
                 'ne': 'северо-восточный',
                 'e': 'восточный',
                 'se': 'юго-восточный',
                 's': 'южный',
                 'sw': 'юго-западный',
                 'w': 'западный',
                 'x': 'штиль'}

dict_condition = {'clear': 'Ясно',
                  'partly-cloudy': 'Малооблачно',
                  'cloudy': 'Облачно с прояснениями',
                  'overcast': 'Пасмурно',
                  'drizzle': 'Морось',
                  'rain': 'Дождь',
                  'light-rain': 'Небольшой дождь',
                  'moderate-rain': 'Умеренно сильный дождь',
                  'heavy-rain': 'Сильный дождь',
                  'continuous-heavy-rain': 'Длительный сильный дождь',
                  'showers': 'Ливень',
                  'wet-snow': 'Дождь со снегом',
                  'light-snow': 'Небольшой снег',
                  'snow': 'Снег',
                  'snow-showers': 'Снегопад',
                  'hail': 'Град',
                  'thunderstorm': 'Гроза',
                  'thunderstorm-with-rain': 'Дождь с грозой',
                  'thunderstorm-with-hail': 'Гроза с градом'}

times_of_day = {'morning': 'Утром',
                'evening': 'Вечером',
                'day': 'Днём',
                'night': 'Ночью'}
