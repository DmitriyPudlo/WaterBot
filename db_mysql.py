from mysql.connector import connect
from config import HOST, PASSWORD_MYSQL, USER_MYSQL, DATABASE_MYSQL
import db_select


class Weather_db:
    def __init__(self):
        self.conn = connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL)
        self.cursor_db = self.conn.cursor()

    def create_database(self):
        sql_create_database = f'CREATE DATABASE IF NOT EXISTS {DATABASE_MYSQL}'
        self.cursor_db.execute(sql_create_database)
        self.__create_tables()

    def __create_tables(self):
        sql_create_table = db_select.mysql_db_create
        self.cursor_db.execute(sql_create_table)

    def add_user(self, client_id):
        sql_add_user = f"INSERT INTO client (client_id) " \
                       f"VALUES ('{client_id}')"
        self.cursor_db.execute(sql_add_user)
        self.conn.commit()

    def add_lag(self, client_id, lag):
        sql_add_lag = f"UPDATE client SET lag_time = '{lag}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_add_lag)
        self.conn.commit()

    def add_city(self, city):
        sql_add_city = f"INSERT INTO cities (city) " \
                       f"VALUES ('{city}')"
        self.cursor_db.execute(sql_add_city)
        self.conn.commit()

    def add_reiteration(self, city):
        sql_add_reiteration = f"UPDATE cities SET reiteration = 1 WHERE city = '{city}'"
        self.cursor_db.execute(sql_add_reiteration)
        self.conn.commit()

    def new_city(self, client_id, geo_tag):
        lat = geo_tag['lat']
        lon = geo_tag['lon']
        sql_add_lat = f"UPDATE client SET lat = '{lat}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_add_lat)
        sql_add_lon = f"UPDATE client SET lon = '{lon}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_add_lon)
        self.conn.commit()

    def new_time(self, client_id, time):
        sql_new_time = f"UPDATE client SET time = '{time}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_new_time)
        self.conn.commit()

    def get_city(self, client_id):
        sql_get_city = f"SELECT lat, lon FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_get_city)
        geo_tag_db = self.cursor_db.fetchone()
        if not geo_tag_db or not geo_tag_db[0]:
            return False
        self.conn.commit()
        return {'lat': geo_tag_db[0], 'lon': geo_tag_db[1]}

    def get_time(self, client_id):
        sql_get_time = f"SELECT time FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_get_time)
        time = self.cursor_db.fetchone()
        self.conn.commit()
        if not time:
            return False
        return time[0]

    def get_lag(self, client_id):
        sql_get_lag = f"SELECT lag_time FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_get_lag)
        time = self.cursor_db.fetchone()
        self.conn.commit()
        return int(time[0])

    def del_client(self, client_id):
        sql_del_client = f"DELETE FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_del_client)
        self.conn.commit()
