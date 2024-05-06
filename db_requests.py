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

    def update_api_key(self, telegram_id, api_key):
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

    def update_ip_name(self, telegram_id, api_key):
        connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.db_name)
        sql_query = "UPDATE shark_table SET ip_name = %s WHERE telegram_id = %s"
        values = (api_key, str(telegram_id))
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
        connection.close()
