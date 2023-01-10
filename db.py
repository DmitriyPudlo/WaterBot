import psycopg2
from Config import DATABASE, USER, PASSWORD


class Water_db:
    def __init__(self):
        self.conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD)
        self.conn.autocommit = True
        self.cursor_db = self.conn.cursor()

    def __create_db(self):
        sql_create_database = f'CREATE DATABASE {DATABASE}'
        self.cursor_db.execute(sql_create_database)

    def __check_existing_db(self):
        sql_db_exists = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{DATABASE}'"
        self.cursor_db.execute(sql_db_exists)
        if not self.cursor_db.fetchall():
            self.__create_db()

    def create_database(self):
        self.__check_existing_db()
        self.__create_tables()

    def __create_tables(self):
        sql_create_table = 'CREATE TABLE IF NOT EXISTS client (' \
                           'id integer NOT NULL GENERATED ALWAYS AS IDENTITY,' \
                           'client_id INT unique,' \
                           'city VARCHAR(30),' \
                           'time VARCHAR(5))'
        self.cursor_db.execute(sql_create_table)

    def add_user(self, client_id):
        sql_add_user = f"INSERT INTO client (client_id) " \
                       f"VALUES ('{client_id}')" \
                       f"ON CONFLICT (client_id) DO NOTHING"
        self.cursor_db.execute(sql_add_user)

    def new_city(self, client_id, geo_tag):
        sql_add_user = f"UPDATE client SET city = '{geo_tag}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_add_user)

    def new_time(self, client_id, time):
        sql_add_user = f"UPDATE client SET time = '{time}' WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_add_user)

    def get_city(self, client_id):
        sql_check = f"SELECT city FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_check)
        geo_tag_db = self.cursor_db.fetchall()
        print(geo_tag_db)
        geo_tag = geo_tag_db[0]
        print(geo_tag)
        if not geo_tag:
            return False
        else:
            geo_tag = [float(coordinate) for coordinate in geo_tag]
            return geo_tag

    def get_time(self, client_id):
        sql_check = f"SELECT time FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_check)
        time = self.cursor_db.fetchone()
        return time[0]

    def del_client(self, client_id):
        sql_del_client = f"DELETE FROM client WHERE client_id = '{client_id}'"
        self.cursor_db.execute(sql_del_client)