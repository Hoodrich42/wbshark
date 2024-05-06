import requests
from datetime import timedelta, date


class ApiRequest:
    session = requests.Session()

    @staticmethod
    def get_header(api_key):
        headers = {'Authorization': f'{api_key}'}
        return headers

    @staticmethod
    def get_today_date():
        today_date = date.today()
        return today_date

    @staticmethod
    def get_yesterday_date():
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        return yesterday_date

    @staticmethod
    def get_week_ago_date():
        today_date = date.today()
        week_ago_date = today_date - timedelta(days=7)
        return week_ago_date

    @staticmethod
    def get_month_ago_date():
        today_date = date.today()
        month_ago_date = today_date - timedelta(days=30)
        return month_ago_date

    @staticmethod
    def get_3_month_ago_date():
        today_date = date.today()
        month_3_ago_date = today_date - timedelta(days=90)
        return month_3_ago_date

    @staticmethod
    def get_6_month_ago_date():
        today_date = date.today()
        month_6_ago_date = today_date - timedelta(days=180)
        return month_6_ago_date

    @staticmethod
    def get_basket(short_id):
        if 0 <= short_id <= 143:
            basket = '01'
        elif 144 <= short_id <= 287:
            basket = '02'
        elif 288 <= short_id <= 431:
            basket = '03'
        elif 432 <= short_id <= 719:
            basket = '04'
        elif 720 <= short_id <= 1007:
            basket = '05'
        elif 1008 <= short_id <= 1061:
            basket = '06'
        elif 1062 <= short_id <= 1115:
            basket = '07'
        elif 1116 <= short_id <= 1169:
            basket = '08'
        elif 1170 <= short_id <= 1313:
            basket = '09'
        elif 1314 <= short_id <= 1601:
            basket = '10'
        elif 1602 <= short_id <= 1655:
            basket = '11'
        elif 1656 <= short_id <= 1919:
            basket = '12'
        elif 1920 <= short_id <= 2045:
            basket = '13'
        elif 2046 <= short_id <= 2189:
            basket = '14'
        elif 2091 <= short_id <= 2405:
            basket = '15'
        elif 2406 <= short_id <= 2621:
            basket = '16'
        else:
            basket = '17'
        return basket

    def api_ip(self, nm_id, api_key):
        headers = self.get_header(api_key)
        short_id = nm_id // 100000
        basket = self.get_basket(short_id)

        url = f'https://basket-{basket}.wbbasket.ru/vol{short_id}/part{nm_id // 1000}/{nm_id}/info/ru/card.json'
        response = self.session.get(url, headers=headers).json()

        supplier_id = response['selling']['supplier_id']
        url = f'https://static-basket-01.wbbasket.ru/vol0/data/supplier-by-id/{supplier_id}.json'
        response = self.session.get(url, headers=headers).json()

        supplier_name = response['supplierName']
        return supplier_name

    def get_orders(self, api_key, date):
        if date == 'today':
            date_from = self.get_today_date()
        headers = self.get_header(api_key)
        url = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={self.date_from}'
        response = self.session.get(url, headers=headers).json()
        return response
