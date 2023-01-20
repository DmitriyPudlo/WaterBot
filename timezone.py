from datetime import datetime
from db_mysql import Weather_db
import time

ERROR_CORRECTION = 3600

weather_db = Weather_db()


def nice_time(time_):
    if time_ < 10:
        return f'0{time_}'
    return time_


def get_posix_time():
    now = datetime.now()
    posix_datetime = int((now - datetime(1970, 1, 1)).total_seconds())
    print('posix_datetime', posix_datetime)
    return posix_datetime


def add_lag(client_id, posix_time):
    server_posix_time = get_posix_time()
    lag = int((posix_time - server_posix_time) / ERROR_CORRECTION)
    weather_db.add_lag(client_id, lag)


def current_time():
    now_posix = int(time.time())
    now = time.gmtime(now_posix)
    hour = nice_time(now.tm_hour)
    minute = nice_time(now.tm_min)
    now_str = f'{hour}:{minute}'
    return now_str
