from Weather import Weather
from Coordinates import Coordinates
from db import Water_db
import telebot
from datetime import datetime
from Config import TELEGRAM_TOKEN, msg_hello, msg_city, msg_time, msg_complete, city_not_found, time_error, msg_bye
import time


def time_check(time):
    try:
        datetime.strptime(time, '%H:%M')
        return True
    except (ValueError, TypeError):
        return False


coordinates = Coordinates()
water = Weather()
water_db = Water_db()
telebot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, f"{msg_hello}")
    water_db.del_client(message.chat.id)
    telebot.send_message(message.chat.id, f"{msg_city}")


@telebot.message_handler(commands=['stop'])
def stop(message):
    water_db.del_client(message.chat.id)
    telebot.send_message(message.chat.id, f"{msg_bye}")
    telebot.stop_polling()


@telebot.message_handler(content_types=['text'])
def work(message):
    water_db.add_user(message.chat.id)
    geo_tag = water_db.get_city(message.chat.id)
    need_time = water_db.get_time(message.chat.id)
    text = message.text
    if not geo_tag and not need_time:
        geo_tag = coordinates.check_coordinates(text)
        if not geo_tag:
            telebot.send_message(message.chat.id, f"{city_not_found}")
            telebot.send_message(message.chat.id, f"{msg_city}")
            return
        else:
            water_db.new_city(message.chat.id, geo_tag)
            telebot.send_message(message.chat.id, f"{msg_time}")
            return
    if not need_time:
        need_time = text
        if not time_check(need_time):
            telebot.send_message(message.chat.id, f"{time_error}")
            telebot.send_message(message.chat.id, f"{msg_time}")
            return
        else:
            water_db.new_time(message.chat.id, need_time)
            telebot.send_message(message.chat.id, f"{msg_complete}")
            print('GO')
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if current_time == need_time:
                    print('YES')
                    msg = water.check_weather(geo_tag)
                    telebot.send_message(message.chat.id, f"{msg}")
                time.sleep(60)



