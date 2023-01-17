from datetime import datetime
from db import Weather_db
import time
from config import TIMEZONE_TOKEN

ERROR_CORRECTION = 3600

weather_db = Weather_db()


def get_posix_time():
    now = datetime.now()
    posix_datetime = int((now - datetime(1970, 1, 1)).total_seconds())
    print('posix_datetime', posix_datetime)
    return posix_datetime


def add_lag(client_id, posix_time):
    print('posix_time', posix_time)
    server_posix_time = get_posix_time()
    print(f'{posix_time} - {server_posix_time}', (posix_time - server_posix_time))
    lag = int((posix_time - server_posix_time) / ERROR_CORRECTION)
    weather_db.add_lag(client_id, lag)


def current_time(cline_id):
    lag = weather_db.get_lag(cline_id) * ERROR_CORRECTION
    now_posix = int(time.time()) - lag
    now = time.gmtime(now_posix)
    now_str = f'{now.tm_hour}:{now.tm_min}'
    return now_str

class Timezone:
    def __init__(self):
        self.url = 'https://timezoneapi.io/api/timezone/'
        self.token = TIMEZONE_TOKEN

