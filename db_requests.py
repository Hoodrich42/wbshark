import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()


class DbRequest():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    def insert_db(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        insert_dannye = (str(telegram_id), 'none|none', 'none|none', 'none|none', 'none|none', 'none|none')
        sql_query = 'INSERT INTO shark_table(telegram_id, api_key, ip_name, orders_today, sales_today, cancel_today) VALUES(%s, %s, %s, %s, %s, %s)'
        with connection.cursor() as cursor:
            cursor.execute(sql_query, insert_dannye)
            connection.commit()
        connection.close()

    def select_all(self):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT * FROM shark_table;"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            users = cursor.fetchall()
            connection.commit()
        connection.close()
        return users

    def select_orders_today(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT orders_today FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            orders_today = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return orders_today

    def update_orders_today(self, orders_today, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET orders_today = %s WHERE telegram_id = %s"
        values = (orders_today, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()

    def select_sales_today(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT sales_today FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            sales_today = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return sales_today

    def update_sales_today(self, sales_today, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET sales_today = %s WHERE telegram_id = %s"
        values = (sales_today, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()

    def select_cancel_today(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT cancel_today FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            cancel_today = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return cancel_today

    def update_cancel_today(self, cancel_today, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET cancel_today = %s WHERE telegram_id = %s"
        values = (cancel_today, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()

    def select_api_key(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT api_key FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            api_keys_list = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return api_keys_list

    def update_api_key(self, api_key, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET api_key = %s WHERE telegram_id = %s"
        values = (api_key, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()

    def select_ip_name(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT ip_name FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            api_keys_list = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return api_keys_list

    def update_ip_name(self, api_key, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET ip_name = %s WHERE telegram_id = %s"
        values = (api_key, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()

    def select_rezerv(self, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "SELECT rezerv FROM shark_table WHERE telegram_id = %s"
        values = (str(telegram_id),)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            rezerv = cursor.fetchall()[0][0]
            connection.commit()
        connection.close()
        return rezerv

    def update_rezerv(self, new_rezerv, telegram_id):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET rezerv = %s WHERE telegram_id = %s"
        values = (new_rezerv, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()