from bot import telebot
from db_postgres import Weather_db

if __name__ == '__main__':
    print('START')
    db = Weather_db()
    db.create_database()
    telebot.infinity_polling()
