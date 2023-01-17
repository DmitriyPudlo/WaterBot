from weather import Weather
from geocode import Geocode
from db import Weather_db
import telebot
from telebot import types
from config import TELEGRAM_TOKEN
import messages
import time
from city_list import city_list
from timezone import add_lag, current_time

PATTERN_TIME = '^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$'
PATTERN_UPDATE_TIME = '^Изменить время: (([0,1][0-9])|(2[0-3])):[0-5][0-9]$'
PATTERN_UPDATE_CITY = '^Изменить город: \S+'
BUTTONS = ['Help']


def create_markup():
    markup_ = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in BUTTONS:
        markup_.add(key)
    return markup_


def find_updated_time(time_):
    time_ = time_.replace('Изменить время: ', '')
    return time_


def find_updated_city(coordinates):
    coordinates = coordinates.replace('Изменить город: ', '')
    if coordinates in city_list:
        return coordinates
    return False


def send_temperature(client_id):
    while water_db.get_city(client_id) and water_db.get_time(client_id):
        print('GO')
        geo_tag = water_db.get_city(client_id)
        need_time = water_db.get_time(client_id)
        now_time = current_time(client_id)
        print(now_time, need_time)
        if now_time == need_time:
            print('YES')
            msg = weather.check_weather(geo_tag)
            telebot.send_message(client_id, f"{msg}", reply_markup=markup)
        time.sleep(60)


geocode = Geocode()
weather = Weather()
water_db = Weather_db()
telebot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
markup = create_markup()


@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, f"{messages.msg_hello}", reply_markup=markup)
    water_db.del_client(message.chat.id)  # del after released


@telebot.message_handler(commands=['stop'])
def stop(message):
    water_db.del_client(message.chat.id)
    telebot.send_message(message.chat.id, f"{messages.msg_bye}")


@telebot.message_handler(regexp=PATTERN_TIME)
def get_time(message):
    geo_tag = water_db.get_city(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f"{messages.msg_city_first}", reply_markup=markup)
        return
    need_time = message.text
    add_lag(message.chat.id, message.date)
    water_db.new_time(message.chat.id, need_time)
    telebot.send_message(message.chat.id, f"{messages.msg_complete}", reply_markup=markup)
    send_temperature(client_id=message.chat.id)


@telebot.message_handler(func=lambda message: message.text in city_list)
def get_city(message):
    geo_tag = water_db.get_city(message.chat.id)
    need_time = water_db.get_time(message.chat.id)
    if not geo_tag:
        water_db.add_user(message.chat.id)
        geo_tag = geocode.get_coordinates(message.text)
        water_db.new_city(message.chat.id, geo_tag)
        telebot.send_message(message.chat.id, f"{messages.msg_time}", reply_markup=markup)
        return
    elif not need_time:
        telebot.send_message(message.chat.id, f'{messages.time_error}', reply_markup=markup)


@telebot.message_handler(regexp=PATTERN_UPDATE_TIME)
def update_time(message):
    need_time = water_db.get_time(message.chat.id)
    if need_time:
        need_time = find_updated_time(message.text)
        water_db.new_time(message.chat.id, need_time)
        telebot.send_message(message.chat.id, f"{messages.msg_change_time}", reply_markup=markup)


@telebot.message_handler(regexp=PATTERN_UPDATE_CITY)
def update_city(message):
    geo_tag = water_db.get_city(message.chat.id)
    if geo_tag:
        new_city = find_updated_city(message.text)
        if not new_city:
            telebot.send_message(message.chat.id, f"{messages.city_not_found}", reply_markup=markup)
        geo_tag = geocode.get_coordinates(new_city)
        water_db.new_city(message.chat.id, geo_tag)
        telebot.send_message(message.chat.id, f"{messages.msg_change_city}", reply_markup=markup)


@telebot.message_handler(func=lambda message: message.text == 'Help')
def get_help(message):
    telebot.send_message(message.chat.id, f'{messages.msg_help}', reply_markup=markup)
    geo_tag = water_db.get_city(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f'{messages.msg_city}', reply_markup=markup)
        return
    need_time = water_db.get_time(message.chat.id)
    if not need_time:
        telebot.send_message(message.chat.id, f'{messages.msg_time}', reply_markup=markup)


@telebot.message_handler(content_types='text')
def catch_trash(message):
    geo_tag = water_db.get_city(message.chat.id)
    if not geo_tag:
        telebot.send_message(message.chat.id, f'{messages.city_not_found}', reply_markup=markup)
        return
    need_time = water_db.get_time(message.chat.id)
    if not need_time:
        telebot.send_message(message.chat.id, f'{messages.time_error}', reply_markup=markup)
