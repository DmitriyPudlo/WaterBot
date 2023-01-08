from Water import Water
from Coordinates import Coordinates
import telebot
from telebot import types
import random
from datetime import datetime
from Config import TELEGRAM_TOKEN, msg_hello, msg_city, msg_time, msg_complete, city_not_found
import time


def test():
    city = 'Орск'
    coordinates = Coordinates()
    water = Water()
    geo_tag = coordinates.check_coordinates(city)
    if not geo_tag:
        return False
    msg = water.check_weather(geo_tag)
    print(msg)
    return


def time_check(time):
    try:
        datetime.strptime(time, '%H:%M')
        return
    except (TypeError or ValueError):
        return False


telebot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, f"{msg_hello}")
    telebot.send_message(message.chat.id, f"{msg_city}")


@telebot.message_handler(content_types=['text'])
def work(message):
    coordinates = Coordinates()
    water = Water()
    text = message.text
    geo_tag = coordinates.check_coordinates(text)
    if not geo_tag:
        telebot.send_message(message.chat.id, f"{city_not_found}")
        telebot.send_message(message.chat.id, f"{msg_city}")
        return
    telebot.send_message(message.chat.id, f"{msg_time}")
    need_time = message.text
    if time_check(need_time):
        while True:
            time.sleep(1)
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            if current_time == need_time:
                print('YES')
                msg = water.check_weather(geo_tag)
                telebot.send_message(message.chat.id, f"{msg}")

