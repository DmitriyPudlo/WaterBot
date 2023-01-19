# import psycopg2
# import db_select
# from config import DATABASE, USER, PASSWORD
#
#
# class Weather_db:
#     def __init__(self):
#         self.conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD)
#         self.conn.autocommit = True
#         self.cursor_db = self.conn.cursor()
#
#     def __create_db(self):
#         sql_create_database = f'CREATE DATABASE {DATABASE}'
#         self.cursor_db.execute(sql_create_database)
#
#     def __check_existing_db(self):
#         sql_db_exists = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{DATABASE}'"
#         self.cursor_db.execute(sql_db_exists)
#         if not self.cursor_db.fetchall():
#             self.__create_db()
#
#     def create_database(self):
#         self.__check_existing_db()
#         self.__create_tables()
#
#     def __create_tables(self):
#         sql_create_table = db_select.postgres_db_create
#         self.cursor_db.execute(sql_create_table)
#
#     def add_user(self, client_id):
#         sql_add_user = f"INSERT INTO client (client_id) " \
#                        f"VALUES ('{client_id}')" \
#                        f"ON CONFLICT (client_id) DO NOTHING"
#         self.cursor_db.execute(sql_add_user)
#
#     def add_lag(self, client_id, lag):
#         sql_add_lag = f"UPDATE client SET lag_time = '{lag}' WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_add_lag)
#
#     def add_city(self, city):
#         sql_add_city = f"INSERT INTO cities (city) " \
#                        f"VALUES ('{city}')" \
#                        f"ON CONFLICT (city) DO NOTHING"
#         self.cursor_db.execute(sql_add_city)
#
#     def add_reiteration(self, city):
#         sql_add_reiteration = f"UPDATE cities SET reiteration = 1 WHERE city = '{city}'"
#         self.cursor_db.execute(sql_add_reiteration)
#
#     def new_city(self, client_id, geo_tag):
#         lat = geo_tag['lat']
#         lon = geo_tag['lon']
#         sql_add_lat = f"UPDATE client SET lat = '{lat}' WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_add_lat)
#         sql_add_lon = f"UPDATE client SET lon = '{lon}' WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_add_lon)
#
#     def new_time(self, client_id, time):
#         sql_new_time = f"UPDATE client SET time = '{time}' WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_new_time)
#
#     def get_city(self, client_id):
#         sql_get_city = f"SELECT lat, lon FROM client WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_get_city)
#         geo_tag_db = self.cursor_db.fetchone()
#         if not geo_tag_db or not geo_tag_db[0]:
#             return False
#         return {'lat': geo_tag_db[0], 'lon': geo_tag_db[1]}
#
#     def get_time(self, client_id):
#         sql_get_time = f"SELECT time FROM client WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_get_time)
#         time = self.cursor_db.fetchone()
#         if not time:
#             return False
#         return time[0]
#
#     def get_lag(self, client_id):
#         sql_get_lag = f"SELECT lag FROM client WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_get_lag)
#         time = self.cursor_db.fetchone()
#         return int(time[0])
#
#     def del_client(self, client_id):
#         sql_del_client = f"DELETE FROM client WHERE client_id = '{client_id}'"
#         self.cursor_db.execute(sql_del_client)
