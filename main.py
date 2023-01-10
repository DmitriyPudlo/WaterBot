from Bot import telebot
from db import Water_db

if __name__ == '__main__':
    print('START')
    db = Water_db()
    db.create_database()
    telebot.infinity_polling()
