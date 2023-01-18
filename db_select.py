mysql_db_create = 'CREATE TABLE IF NOT EXISTS cities (' \
                  'city_id INT PRIMARY KEY AUTO_INCREMENT,' \
                  'city VARCHAR(100) unique,' \
                  'reiteration int);' \
                  'CREATE TABLE IF NOT EXISTS client (' \
                  'id INT PRIMARY KEY AUTO_INCREMENT,' \
                  'client_id INT unique,' \
                  'lat VARCHAR(15),' \
                  'lon VARCHAR(15),' \
                  'time VARCHAR(5),' \
                  'lag_time VARCHAR(15),' \
                  'city_id INT,' \
                  'FOREIGN KEY (city_id) REFERENCES cities (city_id))'

postgres_db_create = 'CREATE TABLE IF NOT EXISTS cities (' \
                     'city_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,' \
                     'city VARCHAR(100) unique,' \
                     'reiteration int,' \
                     'CONSTRAINT users_pkey PRIMARY KEY (city_id));' \
                     'CREATE TABLE IF NOT EXISTS client (' \
                     'id integer NOT NULL GENERATED ALWAYS AS IDENTITY,' \
                     'client_id INT unique,' \
                     'lat VARCHAR(15),' \
                     'lon VARCHAR(15),' \
                     'time VARCHAR(5),' \
                     'lag_time VARCHAR(10),' \
                     'city_id int,' \
                     'FOREIGN KEY (city_id) REFERENCES cities (city_id))'
