from db_requests import *
from wb_requests import *
from datetime import timedelta, date

db_query = DbRequest()
api_query = ApiRequest()


class Notifications:

    @staticmethod
    def get_item_data(item):
        nm_id = item['nmId']
        item_number = item['srid']
        date_item = item['date']
        subject = item['subject']
        barcode = item['barcode']
        category = item['category']
        brand = item["brand"]
        amount = int(item['priceWithDisc'])
        supplier_article = item["supplierArticle"]
        address = f'🌐 {item["warehouseName"]} → {item["regionName"]}'
        date_item_for_msg = f'{date_item.split("T")[0].split("-")[2]}.' \
                            f'{date_item.split("T")[0].split("-")[1]}.' \
                            f'{date_item.split("T")[0].split("-")[0]} ' \
                            f'{date_item.split("T")[1]}'
        return nm_id, item_number, date_item, subject, barcode, category, brand, amount, supplier_article, address, \
            date_item_for_msg

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
    def get_month_ago_dates():
        month_dates = []
        today_date = date.today()
        for i in range(31):
            month_ago_date = today_date - timedelta(days=i)
            month_dates.append(str(month_ago_date))
        return month_dates

    @staticmethod
    def get_cancel_list(orders, sales):
        canceled_list = []
        for item in orders:
            if 'Возврат' in item['orderType'] or 'возврат' in item['orderType'] or item['isCancel']:
                canceled_list.append(item)
        for item in sales:
            if item['saleID'][0] == 'R' or 'Возврат' in item['orderType'] or 'возврат' in item['orderType']:
                canceled_list.append(item)
        return canceled_list

    def get_items_lists(self, item_list):
        today_date = self.get_today_date()
        yesterday_date = self.get_yesterday_date()
        items_list_today = []
        items_list_yesterday = []
        for item in item_list:
            if item['date'].split('T')[0] == today_date:
                items_list_today.append(item)
            if item['date'].split('T')[0] == yesterday_date:
                items_list_yesterday.append(item)
        return items_list_today, items_list_yesterday

    @staticmethod
    def today_count(items_today, nm_id):
        cur_artikul_today_count = 0
        cur_artikul_today_amout = 0
        today_count = 0
        today_amount = 0
        for item in items_today:
            if item['nmId'] == nm_id:
                cur_artikul_today_count += 1
                cur_artikul_today_amout += int(item['priceWithDisc'])
            today_count += 1
            today_amount += int(item['priceWithDisc'])
        cur_artikul = f'{cur_artikul_today_count} на {cur_artikul_today_amout}₽'
        all_today = f'{today_count} на {today_amount}₽'
        return cur_artikul, all_today

    @staticmethod
    def yesterday_count(items_yesterday, nm_id):
        count = 0
        amount = 0
        for item in items_yesterday:
            if item['nmId'] == nm_id:
                count += 1
                amount += int(item['priceWithDisc'])
        yesterday_cur_artikul = f'{count} на {amount}₽'
        return yesterday_cur_artikul

    @staticmethod
    def abc_calculation(response_prodazhi, nm_id):
        oborot_tovara = 0
        persent_abc = ''
        oborot = 0
        for item in response_prodazhi:
            # if response[i]['brand'] == response_prodazhi[j]['brand']:
            if item['saleID'][0] == 'S':
                oborot += item['priceWithDisc']
            if nm_id == item['nmId']:
                if item['saleID'][0] == 'S':
                    oborot_tovara += item['priceWithDisc']
        try:
            abc_analiz = round(oborot_tovara * 100 / oborot, 2)
            if abc_analiz > 7:
                color_abc = '🟩'
            elif 5 < abc_analiz <= 7:
                color_abc = '🟧'
            else:
                color_abc = '🟥'
            if oborot != 0 and oborot_tovara != 0:
                persent_abc = f'{color_abc}ABC анализ: ({abc_analiz}%)\n'
            else:
                persent_abc = 'ABC анализ: (0%)\n'
        except:
            persent_abc = f'0\n'
        return persent_abc

    @staticmethod
    def vykup_3_month(response_prodazhi, orders, nm_id):
        vykup = ''
        all_quant = 0
        vykup_quant = 0
        for prodazha in response_prodazhi:
            if nm_id == prodazha['nmId']:
                if prodazha['saleID'][0] == 'S':
                    vykup_quant += 1
        for order in orders:
            if nm_id == order['nmId']:
                all_quant += 1
        if all_quant != 0 and vykup_quant != 0:
            vykup = f'💎 Выкуп за 3 мес: {round(vykup_quant * 100 / all_quant, 2)}% ({vykup_quant}/{all_quant})\n'
        else:
            vykup = f'💎 Выкуп за 3 мес: 0% (0/0)\n'
        return vykup

    @staticmethod
    def check_stock(stock, nm_id):
        sum_to_klient = 0
        sum_from_klient = 0
        all_sklad = ''
        summ = 0
        for stock_item in stock:
            if stock_item != 0 and stock_item['nmId'] == nm_id:
                if stock_item['quantity'] > 0:
                    all_sklad = all_sklad + f'📦 {stock_item["warehouseName"]}: {stock_item["quantity"]}\n'
                    summ += stock_item["quantity"]
                sum_to_klient += stock_item['inWayToClient']
                sum_from_klient += stock_item['inWayFromClient']
        return all_sklad, summ, sum_to_klient, sum_from_klient

    def order_cheking(self, type, telegram_id, api_key_number, api_key):
        orders_3_month = api_query.get_orders(api_key, '3_month')
        sales_3_month = api_query.get_sales(api_key, '3_month')
        stock = api_query.get_stock(api_key)

        today_date = self.get_today_date()
        month_ago_dates = self.get_month_ago_dates()
        yesterday_date = self.get_yesterday_date()

        orders_1_month = []
        for order in orders_3_month:
            if order['date'].split('T')[0] in month_ago_dates:
                orders_1_month.append(order)

        if type == 'order':
            today_list = db_query.select_orders_today(telegram_id).split('|')[api_key_number].split(',')
            items_list_today, items_list_yesterday = self.get_items_lists(orders_3_month)
        elif type == 'sale':
            today_list = db_query.select_sales_today(telegram_id).split('|')[api_key_number].split(',')
            items_list_today, items_list_yesterday = self.get_items_lists(sales_3_month)
        elif type == 'cancel':
            today_list = db_query.select_cancel_today(telegram_id).split('|')[api_key_number].split(',')
            canceled_3_month = self.get_cancel_list(orders_3_month, sales_3_month)
            items_list_today, items_list_yesterday = self.get_items_lists(canceled_3_month)

        for item in items_list_today:
            nm_id, order_number, date_order, subject, barcode, category, brand, \
                amount, supplier_article, address, date_order_for_msg = self.get_item_data(item)

            if not order_number in today_list:
                if 'none' in today_list:
                    today_list = [order_number]
                else:
                    today_list.append(order_number)
                items_count = len(today_list)

                # Получаем фото товара
                img = api_query.api_img(nm_id)
                # Получаем рейтинг и отзывы
                rate, reviews = api_query.api_rate_and_reviews(nm_id)

                # Количество товаров и сумма за сегодня
                # количество и стоимость определенного артикула за сегодня и за вчера
                cur_artikul_today, all_today = self.today_count(items_list_today, nm_id)
                cur_artikul_yesterday = self.yesterday_count(items_list_yesterday, nm_id)

                # Получаем ABC анализ и процент выкупа
                abc_analyz = self.abc_calculation(sales_3_month, nm_id)
                vykup = self.vykup_3_month(sales_3_month, orders_3_month, nm_id)

                # Получаем остатки товара
                all_sklad, summ, sum_to_klient, sum_from_klient = self.check_stock(stock, nm_id)

                # Резерв
                rezerv_kolich = rezerv_calculate(orders_1_month, nm_id, summ, rezerv_days)


        return canceled_3_month
