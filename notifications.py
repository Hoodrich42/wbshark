from db_requests import *
from wb_requests import *
from datetime import timedelta, date
import pandas as pd
import telebot

bot_token = os.getenv('TOKEN')
bot = telebot.TeleBot(bot_token)

db_query = DbRequest()
api_query = ApiRequest()


class Notifications:

    @staticmethod
    def get_comission():
        dict_categories = {}
        comission_file = pd.ExcelFile('test_bot/сomission.xlsx')
        comission_file = comission_file.parse()
        for i in comission_file['Категория']:
            if i in dict_categories.keys():
                pass
            else:
                if not pd.isnull(i):
                    dict_categories[i] = comission_file.loc[comission_file['Категория'] == i, 'Склад WB, %'].unique()[0]
        return dict_categories

    dict_categories = get_comission()

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
        return str(today_date)

    @staticmethod
    def get_yesterday_date():
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        return str(yesterday_date)

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

    @staticmethod
    def rezerv_calculate(orders_rezerv, nm_id, summ, rezerv_days):
        count_rezerv = 0
        for i in range(len(orders_rezerv)):
            if orders_rezerv[i]['nmId'] == nm_id:
                count_rezerv += 1

        rezerv_kolich = count_rezerv / 30 * rezerv_days - summ
        if rezerv_kolich < 0:
            rezerv_kolich = 0
        return rezerv_kolich

    @staticmethod
    def update_item_tooday(today_items_list, telegram_id, m, type_response):
        # Делаем проверку чтобы очистить tovary_zakaz_today
        if len(today_items_list) > 0:
            fl_update_item = True
            if type_response == 'order':
                tovary_today = db_query.select_orders_today(telegram_id).split('|')
            elif type_response == 'sale':
                tovary_today = db_query.select_sales_today(telegram_id).split('|')
            elif type_response == 'cancel':
                tovary_today = db_query.select_cancel_today(telegram_id).split('|')
            items_today_list = tovary_today[m].split(',')
            for item in today_items_list:
                order_number = item['srid']
                if order_number in items_today_list:
                    fl_update_item = False
            if fl_update_item:
                update_dannye_item = 'none'
                tovary_today[m] = update_dannye_item
                update_item = ''
                for i in range(len(tovary_today)):
                    if i + 1 == len(tovary_today):
                        update_item += f'{tovary_today[i]}'
                    else:
                        update_item += f'{tovary_today[i]}|'
                if type_response == 'order':
                    db_query.update_orders_today(update_item, telegram_id)
                elif type_response == 'sale':
                    db_query.update_sales_today(update_item, telegram_id)
                elif type_response == 'cancel':
                    db_query.update_cancel_today(update_item, telegram_id)

    @staticmethod
    def get_msg_plus(items_today, today_list, nm_id, comission, type):
        # Склеиваем заказы с одинаковым артикулом
        msg_plus = '\n\n➕ в том числе 👇🏻\n\n'
        count_plus = 0
        for i in range(len(items_today)):
            if nm_id == items_today[i]['nmId'] and not items_today[i]['srid'] in today_list:
                count_plus += 1
                today_list.append(items_today[i]['srid'])
                date_order_for_msg_plus = f'{items_today[i]["date"].split("T")[0].split("-")[2]}.' \
                                          f'{items_today[i]["date"].split("T")[0].split("-")[1]}.' \
                                          f'{items_today[i]["date"].split("T")[0].split("-")[0]} ' \
                                          f'{items_today[i]["date"].split("T")[1]}'
                address_plus = f'🌐 {items_today[i]["warehouseName"]} → {items_today[i]["regionName"]}'
                if type == 'order':
                    third_str = f'🛒Заказ[{len(today_list)}]: {int(items_today[i]["priceWithDisc"])}₽\n'
                if type == 'sale':
                    third_str = f'✅ Выкуп[{len(today_list)}]: {int(items_today[i]["priceWithDisc"])}₽\n'
                if type == 'cancel':
                    third_str = f'🚫 Отмена[{len(today_list)}]: {int(items_today[i]["priceWithDisc"])}₽\n'
                msg_plus += f'{date_order_for_msg_plus}\n' \
                            f'{third_str}' \
                            f'💼 Комиссия (базовая): {comission}%\n' \
                            f'{address_plus}\n\n'
                if count_plus == 4:
                    break

        if count_plus == 0:
            msg_plus = ''

        return msg_plus

    def order_cheking(self, type, telegram_id, api_key_number, api_key, stock, orders_3_month, sales_3_month):
        rezerv_days = int(db_query.select_rezerv(telegram_id).split('|')[api_key_number])
        short_mode = db_query.select_short_mode(telegram_id).split('|')[api_key_number]
        ip_name = db_query.select_ip_name(telegram_id).split('|')

        month_ago_dates = self.get_month_ago_dates()

        orders_1_month = []
        for order in orders_3_month:
            if order['date'].split('T')[0] in month_ago_dates:
                orders_1_month.append(order)

        if type == 'order':
            items_list_today, items_list_yesterday = self.get_items_lists(orders_3_month)
        elif type == 'sale':
            items_list_today, items_list_yesterday = self.get_items_lists(sales_3_month)
        elif type == 'cancel':
            canceled_3_month = self.get_cancel_list(orders_3_month, sales_3_month)
            items_list_today, items_list_yesterday = self.get_items_lists(canceled_3_month)
            print(items_list_today)

        self.update_item_tooday(items_list_today, telegram_id, api_key_number, type)

        if type == 'order':
            today_list_full = db_query.select_orders_today(telegram_id).split('|')
            today_list = today_list_full[api_key_number].split(',')
        elif type == 'sale':
            today_list_full = db_query.select_sales_today(telegram_id).split('|')
            today_list = today_list_full[api_key_number].split(',')
            items_list_today, items_list_yesterday = self.get_items_lists(sales_3_month)
        elif type == 'cancel':
            today_list_full = db_query.select_cancel_today(telegram_id).split('|')
            today_list = today_list_full[api_key_number].split(',')

        for item in items_list_today:
            nm_id, order_number, date_order, subject, barcode, category, brand, \
                amount, supplier_article, address, date_order_for_msg = self.get_item_data(item)

            if not (order_number in today_list):
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

                # Комиссия
                try:
                    comission = self.dict_categories[f"{category}"]
                except:
                    comission = 0

                # Резерв
                rezerv_kolich = self.rezerv_calculate(orders_1_month, nm_id, summ, rezerv_days)

                msg_plus = self.get_msg_plus(items_list_today, today_list, nm_id, comission, type)

                # Обновляем список заказов за сегодня в базе данных
                updated_items_today = ''
                for i in range(len(today_list)):
                    if i + 1 == len(today_list):
                        updated_items_today += f'{today_list[i]}'
                    else:
                        updated_items_today += f'{today_list[i]},'

                today_list_full[api_key_number] = updated_items_today

                updated_items_today_list = ''
                for i in range(len(today_list_full)):
                    if i + 1 == len(today_list_full):
                        updated_items_today_list += f'{today_list_full[i]}'
                    else:
                        updated_items_today_list += f'{today_list_full[i]}|'

                if type == 'order':
                    db_query.update_orders_today(updated_items_today_list, telegram_id)
                    third_str = f'🛒Заказ[{items_count}]: {amount}₽\n'
                if type == 'sale':
                    db_query.update_sales_today(updated_items_today_list, telegram_id)
                    third_str = f'✅ Выкуп[{items_count}]: {amount}₽\n'
                if type == 'cancel':
                    db_query.update_cancel_today(updated_items_today_list, telegram_id)
                    third_str = f'🚫 Отмена[{items_count}]: {amount}₽\n'

                if short_mode == 'true':
                    msg = f'{ip_name[api_key_number]}\n\n' \
                          f'{date_order_for_msg}\n' \
                          f'{third_str}' \
                          f'📈 Сегодня: {all_today}\n' \
                          f'🆔 Арт: <a href="https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=XS">{nm_id}</a> ' \
                          f'(<a href="https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=XS">{supplier_article}</a>)\n' \
                          f'📁{subject}\n' \
                          f'{address}\n\n' \
                          f'{all_sklad}' \
                          f'📦 Всего: {summ}\n' \
                          f'🚗 Пополните склад на {int(rezerv_kolich)} шт.' \
                          f'{msg_plus}'
                else:
                    msg = f'{ip_name[api_key_number]}\n\n' \
                          f'{date_order_for_msg}\n' \
                          f'{third_str}' \
                          f'📈 Сегодня: {all_today}\n' \
                          f'🆔 Арт: <a href="https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=XS">{nm_id}</a>\n' \
                          f'📁{subject}\n' \
                          f'🏷{brand} \ <a href="https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=XS">{supplier_article}</a>\n' \
                          f'#️⃣ Баркод: {barcode}\n' \
                          f'⭐️ Рейтинг: {rate}\n' \
                          f'💬 Отзывы: {reviews}\n' \
                          f'💵 Сегодня таких: {cur_artikul_today}\n' \
                          f'💶 Вчера таких: {cur_artikul_yesterday}\n' \
                          f'{abc_analyz}' \
                          f'💼 Комиссия (базовая): {comission}%\n' \
                          f'{vykup}' \
                          f'{address}\n' \
                          f'🚛 В пути до клиента: {sum_to_klient}\n' \
                          f'🚚 В пути возвраты: {sum_from_klient}\n\n' \
                          f'{all_sklad}' \
                          f'📦 Всего: {summ}\n' \
                          f'🚗 Пополните склад на {int(rezerv_kolich)} шт.' \
                          f'{msg_plus}'

                bot.send_photo(telegram_id, img, msg, parse_mode='html')

