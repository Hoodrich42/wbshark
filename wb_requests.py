from urllib.request import urlopen
import requests
from datetime import timedelta, date
from PIL import Image


class ApiRequest:
    headers_rate = {'cookie': "_wbauid=9648825711703315310; ___wbu=71f7047b-8a64-4fb9-9edb-fa3fcab99814.1703315311; BasketUID=dd5fc623b937492181c3059109551956; __wba_s=1; _wbSes=CfDJ8EB%2FQ73qxdJGob0wNMO1ZqYH2s2%2Bx7RbKsMG%2FeDo3%2B9SHNdEduCisWzx5Kr5RItRPZ2W3xgKtMGNEMyYE0L42IDb1REzN4mA%2BPFncv43ukwVn%2BzcD5ru7RBpRj3bXaUipFrCUTAbnz3Mlm1g6T36ZDYdesEySWaOeJ9pMcSSodjK; WILDAUTHNEW_V3=314F211E1B20517C03ABB56D95134645674B053F735F24D8354B6177B2EDBD9B3F49D32459AA1174A2B839EB359141A9EC2CAF3B9DF3D495F63836B6C38275B0B45B67C3153FCC243EE59DCDCE88C331FB3FC75241911ACFC891A4F7ED1F6BCE8D9FDDF6F446DFC6F342C5116F6CADA5E261AC785415513677D024E3641D81543C13574F233634B88F87EC8FBEE499B6E92158A67191AE766CD32AD8CF7EFEBE50F0D7B710F656D62D177AD1842CA6CAE856B267D5F6CFD0CD12D01700A1A58D8528625868048BBC81F78A68E22B13C986B095E2426BF8706DAA01626362BFDE8FA1CE45623B5532F714289A9D961A674A0FE5FE362D68A31268799183C6D91EC659B865E3A2390791019791F3E06279C111BCEF01759E2A5DCB01BC8DC78E95BED7D0E1462D7830AA10539B99878A9174587BFCBA0C5BC786ACD6EAAD230840C2122895; wbx-validation-key=d17d371e-804b-4750-85d5-ebea51766423; um=uid%3Dw7TDssOkw7PCu8KwwrXCssK1wrPCuMK2wrE%253d%3Aproc%3D100%3Aehash%3D; ___wbs=8a3b219d-40dc-4b22-b8f2-e2f27ae403d1.1710331628"}
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
        today_date = self.get_today_date()
        if date == '30_days':
            date_from = self.get_month_ago_date()
        elif date == '3_month':
            date_from = self.get_3_month_ago_date()
        headers = self.get_header(api_key)
        url = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={date_from}&dateTo={today_date}'
        response = self.session.get(url, headers=headers).json()
        return response

    def get_sales(self, api_key, date):
        today_date = self.get_today_date()
        if date == '30_days':
            date_from = self.get_month_ago_date()
        elif date == '3_month':
            date_from = self.get_3_month_ago_date()
        headers = self.get_header(api_key)
        url = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date_from}&dateTo={today_date}'
        response = self.session.get(url, headers=headers).json()
        return response

    def api_pics(self, nm_id):
        url_rate = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=12358506&spp=28&nm={nm_id}'
        response = self.session.get(url_rate, headers=self.headers_rate)
        response = response.json()
        pics = response['data']['products'][0]['pics']
        return pics

    def api_img(self, nm_id):
        short_id = nm_id // 100000
        basket = self.get_basket(short_id)

        pics = self.api_pics(nm_id)

        links = []
        if pics <= 3:
            for i in range(pics):
                url = f'https://basket-{basket}.wbbasket.ru/vol{short_id}/part{nm_id // 1000}/{nm_id}/images/big/{i+1}.webp'
                links.append(url)
        else:
            for i in range(3):
                url = f'https://basket-{basket}.wbbasket.ru/vol{short_id}/part{nm_id // 1000}/{nm_id}/images/big/{i + 1}.webp'
                links.append(url)

        img_size = (1000, 450)
        img = Image.new('RGB', img_size, '#ffffff')

        otstup = 0
        for j in links:
            try:
                image = Image.open(urlopen(j))
                new_image = image.resize((320, 437))
                img.paste(new_image, (otstup + 7, 5))
                otstup += 330
            except:
                pass

        return img

    def api_rate_and_reviews(self, nm_id):
        url_rate = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=12358506&spp=28&nm={nm_id}'
        response = self.session.get(url_rate, headers=self.headers_rate)
        response = response.json()
        rate = response["data"]["products"][0]["reviewRating"]
        reviews = response["data"]["products"][0]["feedbacks"]
        return rate, reviews

    def get_stock(self, api_key):
        month_6_ago_date = self.get_6_month_ago_date()
        headers = self.get_header(api_key)
        url = f'https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom={month_6_ago_date}'
        response = self.session.get(url, headers=headers).json()
        return response
