import re
from Weather import Weather
from Geocode import Geocode
from db import Water_db
import telebot
from telebot import types
from datetime import datetime
from Config import TELEGRAM_TOKEN
import Messages
import time
from city_list import city_list

PATTERN_TIME = '^\d{1,2}:\d{2}$'
PATTERN_UPDATE_TIME = '^Изменить время: \d{1,2}:\d{2}$'
PATTER_FIND_TIME = '\d{1,2}:\d{2}'
PATTERN_UPDATE_CITY = '^Изменить город: \S+'
ERROR_CORRECTION = 3600
BUTTONS = ['Help']


def create_markup():
    markup_ = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in BUTTONS:
        markup_.add(key)
    return markup_


def time_check(time_):
    try:
        datetime.strptime(time_, '%H:%M')
        return True
    except (ValueError, TypeError):
        return False


def find_updated_time(time_):
    time_str = re.search(PATTER_FIND_TIME, time_)
    time_ = time_str.group()
    return time_


def find_updated_city(coordinates):
    coordinates = coordinates.replace('Изменить город: ', '')
    if coordinates in city_list:
        return coordinates
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


geocode = Geocode()
water = Weather()
water_db = Water_db()
telebot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
markup = create_markup()


@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, f"{Messages.msg_hello}", reply_markup=markup)
    water_db.del_client(message.chat.id)  # del after released
    telebot.send_message(message.chat.id, f"{Messages.msg_city}", reply_markup=markup)
    return


@telebot.message_handler(commands=['stop'])
def stop(message):
    water_db.del_client(message.chat.id)
    telebot.send_message(message.chat.id, f"{Messages.msg_bye}")


@telebot.message_handler(regexp=PATTERN_TIME)
def get_time(message):
    geo_tag = water_db.get_city(message.chat.id)
    need_time = water_db.get_time(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f"{Messages.msg_city_first}", reply_markup=markup)
        return
    elif not need_time:
        need_time = message.text
        if not time_check(need_time):
            telebot.send_message(message.chat.id, f"{Messages.time_error}", reply_markup=markup)
            return
        find_lag(message.chat.id, message.date)
        water_db.new_time(message.chat.id, need_time)
        telebot.send_message(message.chat.id, f"{Messages.msg_complete}", reply_markup=markup)
        while water_db.get_city(message.chat.id) and water_db.get_time(message.chat.id):
            print('GO')
            geo_tag = water_db.get_city(message.chat.id)
            need_time = water_db.get_time(message.chat.id)
            now_time = current_time(message.chat.id)
            if now_time == need_time:
                print('YES')
                msg = water.check_weather(geo_tag)
                telebot.send_message(message.chat.id, f"{msg}", reply_markup=markup)
            time.sleep(60)


@telebot.message_handler(func=lambda message: message.text in city_list)
def get_city(message):
    geo_tag = water_db.get_city(message.chat.id)
    need_time = water_db.get_time(message.chat.id)
    if not geo_tag:
        water_db.add_user(message.chat.id)
        geo_tag = geocode.get_coordinates(message.text)
        water_db.new_city(message.chat.id, geo_tag)
        telebot.send_message(message.chat.id, f"{Messages.msg_time}", reply_markup=markup)
        return
    elif not need_time:
        telebot.send_message(message.chat.id, f'{Messages.time_error}', reply_markup=markup)
        return


@telebot.message_handler(regexp=PATTERN_UPDATE_TIME)
def update_time(message):
    need_time = water_db.get_time(message.chat.id)
    if need_time:
        need_time = find_updated_time(message.text)
        if not time_check(need_time):
            telebot.send_message(message.chat.id, f"{Messages.time_error}", reply_markup=markup)
        water_db.new_time(message.chat.id, need_time)
        telebot.send_message(message.chat.id, f"{Messages.msg_change_time}", reply_markup=markup)


@telebot.message_handler(regexp=PATTERN_UPDATE_CITY)
def update_city(message):
    geo_tag = water_db.get_city(message.chat.id)
    if geo_tag:
        new_city = find_updated_city(message.text)
        if not new_city:
            telebot.send_message(message.chat.id, f"{Messages.city_not_found}", reply_markup=markup)
        geo_tag = geocode.get_coordinates(new_city)
        water_db.new_city(message.chat.id, geo_tag)
        telebot.send_message(message.chat.id, f"{Messages.msg_change_city}", reply_markup=markup)


@telebot.message_handler(func=lambda message: message.text == 'Help')
def get_help(message):
    telebot.send_message(message.chat.id, f'{Messages.msg_help}', reply_markup=markup)
    geo_tag = water_db.get_city(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f'{Messages.msg_city}', reply_markup=markup)
        return
    need_time = water_db.get_time(message.chat.id)
    if not need_time:
        telebot.send_message(message.chat.id, f'{Messages.msg_time}', reply_markup=markup)


@telebot.message_handler(content_types='text')
def catch_trash(message):
    geo_tag = water_db.get_city(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f'{Messages.city_not_found}', reply_markup=markup)
        return
    need_time = water_db.get_time(message.chat.id)
    if not need_time:
        telebot.send_message(message.chat.id, f'{Messages.time_error}', reply_markup=markup)
