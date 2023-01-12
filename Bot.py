from Weather import Weather
from Geocode import Geocode
from db import Water_db
import telebot
from datetime import datetime
from Config import TELEGRAM_TOKEN
from Messages import msg_hello, msg_city, msg_time, msg_complete, city_not_found, time_error, msg_bye
import time

PATTERN = '\d{1,2}:\d{2}'
ERROR_CORRECTION = 3600


def time_check(time_):
    try:
        datetime.strptime(time_, '%H:%M')
        return True
    except (ValueError, TypeError):
        return False


def get_posix_time():
    now = datetime.now()
    posix_datetime = int((now - datetime(1970, 1, 1)).total_seconds())
    return posix_datetime


def find_lag(client_id, posix_time):
    server_posix_time = get_posix_time()
    lag = (posix_time - server_posix_time) // ERROR_CORRECTION
    water_db.add_lag(client_id, lag)
    return


def current_time(cline_id):
    lag = water_db.get_lag(cline_id) * ERROR_CORRECTION
    now_posix = int(time.time()) - lag
    now = time.gmtime(now_posix)
    now_str = f'{now.tm_hour}:{now.tm_min}'
    return now_str


coordinates = Geocode()
water = Weather()
water_db = Water_db()
telebot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, f"{msg_hello}")
    water_db.del_client(message.chat.id)  # del after released
    telebot.send_message(message.chat.id, f"{msg_city}")


@telebot.message_handler(commands=['stop'])
def stop(message):
    water_db.del_client(message.chat.id)
    telebot.send_message(message.chat.id, f"{msg_bye}")


@telebot.message_handler(regexp=PATTERN)
def get_time(message):
    geo_tag = water_db.get_city(message.chat.id)
    find_lag(message.chat.id, message.date)
    if geo_tag:
        need_time = message.text
        if not time_check(need_time):
            telebot.send_message(message.chat.id, f"{time_error}")
            return
        else:
            water_db.new_time(message.chat.id, need_time)
            telebot.send_message(message.chat.id, f"{msg_complete}")
            print('GO')
            while True:
                now = current_time(message.chat.id)
                if now == need_time:
                    print('YES')
                    msg = water.check_weather(geo_tag)
                    telebot.send_message(message.chat.id, f"{msg}")
                time.sleep(60)
    else:
        telebot.send_message(message.chat.id, f"{city_not_found}")
        return


@telebot.message_handler(content_types=['text'])
def work(message):
    water_db.add_user(message.chat.id)
    geo_tag = water_db.get_city(message.chat.id)
    text = message.text
    if not geo_tag:
        geo_tag = coordinates.check_coordinates(text)
        if not geo_tag:
            telebot.send_message(message.chat.id, f"{city_not_found}")
            return
        else:
            water_db.new_city(message.chat.id, geo_tag)
            telebot.send_message(message.chat.id, f"{msg_time}")
            return
    else:
        telebot.send_message(message.chat.id, f"{msg_time}")
