from mysql.connector import connect
from config import HOST, PASSWORD_MYSQL, USER_MYSQL, DATABASE_MYSQL
import db_select


class Weather_db:
    def create_database(self):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_create_database = f'CREATE DATABASE IF NOT EXISTS {DATABASE_MYSQL}'
                cursor_db.execute(sql_create_database)
                self.__create_tables()

    def __create_tables(self):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_create_table = db_select.mysql_db_create
                cursor_db.execute(sql_create_table)

    def add_user(self, client_id):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_add_user = f"INSERT INTO client (client_id) " \
                               f"VALUES ('{client_id}')"
                cursor_db.execute(sql_add_user)
                conn.commit()

    def add_lag(self, client_id, lag):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_add_lag = f"UPDATE client SET lag_time = '{lag}' WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_add_lag)
                conn.commit()

    def add_city(self, city):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_add_city = f"INSERT INTO cities (city) " \
                               f"VALUES ('{city}')"
                cursor_db.execute(sql_add_city)
                conn.commit()

    def add_reiteration(self, city):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_add_reiteration = f"UPDATE cities SET reiteration = 1 WHERE city = '{city}'"
                cursor_db.execute(sql_add_reiteration)
                conn.commit()

    def new_city(self, client_id, geo_tag):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                lat = geo_tag['lat']
                lon = geo_tag['lon']
                sql_add_lat = f"UPDATE client SET lat = '{lat}' WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_add_lat)
                sql_add_lon = f"UPDATE client SET lon = '{lon}' WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_add_lon)
                conn.commit()

    def new_time(self, client_id, time):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_new_time = f"UPDATE client SET time = '{time}' WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_new_time)
                conn.commit()

    def get_city(self, client_id):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_get_city = f"SELECT lat, lon FROM client WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_get_city)
                geo_tag_db = cursor_db.fetchone()
                if not geo_tag_db or not geo_tag_db[0]:
                    return False
                conn.commit()
                return {'lat': geo_tag_db[0], 'lon': geo_tag_db[1]}

    def get_time(self, client_id):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_get_time = f"SELECT time FROM client WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_get_time)
                time = cursor_db.fetchone()
                conn.commit()
                if not time:
                    return False
                return time[0]

    def get_lag(self, client_id):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_get_lag = f"SELECT lag_time FROM client WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_get_lag)
                time = cursor_db.fetchone()
                conn.commit()
                return int(time[0])

    def del_client(self, client_id):
        with connect(host=HOST, user=USER_MYSQL, password=PASSWORD_MYSQL, database=DATABASE_MYSQL) as conn:
            with conn.cursor() as cursor_db:
                sql_del_client = f"DELETE FROM client WHERE client_id = '{client_id}'"
                cursor_db.execute(sql_del_client)
                conn.commit()
