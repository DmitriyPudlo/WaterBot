from datetime import datetime
import time
import pytz
from timezonefinder import TimezoneFinder


tf = TimezoneFinder()


def nice_time(time_):
    if time_ < 10:
        return f'0{time_}'
    return time_


def find_lag(lat, lon):
    tz = tf.timezone_at(lng=lon, lat=lat)
    pytz_tz = pytz.timezone(tz)
    print(pytz_tz)
    client_time = datetime.now(pytz_tz)
    pytz_lag_str = client_time.strftime('%z')
    pytz_lag = int(pytz_lag_str)
    hour = pytz_lag // 100
    minute = pytz_lag % 100
    lag = hour * 60 + minute
    return lag


def current_time(lag):
    server_time_posix = int(time.time())
    sec_lag = lag * 60
    now_time_posix = server_time_posix + sec_lag
    now_time = time.gmtime(now_time_posix)
    hour = nice_time(now_time.tm_hour)
    minute = nice_time(now_time.tm_min)
    need_time_str = f'{hour}:{minute}'
    return need_time_str


