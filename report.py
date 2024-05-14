from datetime import timedelta, date
from db_requests import *

db_query = DbRequest()

class Report:
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
    def get_week_ago_dates():
        week_days = []
        today_date = date.today()
        for i in range(8):
            month_ago_date = today_date - timedelta(days=i)
            week_days.append(str(month_ago_date))
        return week_days

    @staticmethod
    def get_month_ago_dates():
        month_dates = []
        today_date = date.today()
        for i in range(31):
            month_ago_date = today_date - timedelta(days=i)
            month_dates.append(str(month_ago_date))
        return month_dates

    def report(self, orders_30_days, sales_30_days, telegram_id, ip_name):

        today_date = self.get_today_date()
        yesterday_date = self.get_yesterday_date()
        week_ago_dates = self.get_week_ago_dates()

        txt_vrem_hraniliche = ''
        count_orders_today = 0
        summ_orders_today = 0
        count_orders_yesterday = 0
        summ_orders_yesterday = 0
        count_orders_7_days_ago = 0
        summ_orders_7_days_ago = 0
        count_orders_3_month = 0
        summ_orders_3_month = 0
        count_canceled_today = 0
        summ_canceled_today = 0
        count_canceled_yesterday = 0
        summ_canceled_yesterday = 0
        count_canceled_7_days_ago = 0
        summ_canceled_7_days_ago = 0
        count_canceled_3_month = 0
        summ_canceled_3_nomth = 0

        for i in range(len(orders_30_days)):
            if orders_30_days[i]['date'].split('T')[0] == today_date:
                count_orders_today += 1
                summ_orders_today += orders_30_days[i]['priceWithDisc']
            if orders_30_days[i]['date'].split('T')[0] == yesterday_date:
                count_orders_yesterday += 1
                summ_orders_yesterday += orders_30_days[i]['priceWithDisc']
            if orders_30_days[i]['date'].split('T')[0] in week_ago_dates:
                count_orders_7_days_ago += 1
                summ_orders_7_days_ago += orders_30_days[i]['priceWithDisc']
            if 'Возврат' in orders_30_days[i]['orderType'] or 'возврат' in orders_30_days[i]['orderType'] or orders_30_days[i]['isCancel']:
                if orders_30_days[i]['lastChangeDate'].split('T')[0] == today_date:
                    count_canceled_today += 1
                    summ_canceled_today += orders_30_days[i]['priceWithDisc']
                if orders_30_days[i]['lastChangeDate'].split('T')[0] == yesterday_date:
                    count_canceled_yesterday += 1
                    summ_canceled_yesterday += orders_30_days[i]['priceWithDisc']
                if orders_30_days[i]['lastChangeDate'].split('T')[0] in week_ago_dates:
                    count_canceled_7_days_ago += 1
                    summ_canceled_7_days_ago += orders_30_days[i]['priceWithDisc']
                count_canceled_3_month += 1
                summ_canceled_3_nomth += orders_30_days[i]['priceWithDisc']
                txt_vrem_hraniliche += f'R_{orders_30_days[i]["date"].split("T")[0]}_{orders_30_days[i]["nmId"]}_{orders_30_days[i]["subject"]}_{orders_30_days[i]["category"]}_{orders_30_days[i]["regionName"]}_{orders_30_days[i]["brand"]}_{orders_30_days[i]["priceWithDisc"]}_{orders_30_days[i]["srid"]}_{orders_30_days[i]["warehouseName"]},'

            count_orders_3_month += 1
            summ_orders_3_month += orders_30_days[i]['priceWithDisc']
            txt_vrem_hraniliche += f'O_{orders_30_days[i]["date"].split("T")[0]}_{orders_30_days[i]["nmId"]}_{orders_30_days[i]["subject"]}_{orders_30_days[i]["category"]}_{orders_30_days[i]["regionName"]}_{orders_30_days[i]["brand"]}_{orders_30_days[i]["priceWithDisc"]}_{orders_30_days[i]["srid"]}_{orders_30_days[i]["warehouseName"]},'

        count_sales_today = 0
        summ_sales_today = 0
        count_sales_yesterday = 0
        summ_sales_yesterday = 0
        count_sales_7_days_ago = 0
        summ_sales_7_days_ago = 0
        count_sales_3_month = 0
        summ_sales_3_month = 0

        for i in range(len(sales_30_days)):
            if sales_30_days[i]['saleID'][0] == 'S':
                if sales_30_days[i]['date'].split('T')[0] == today_date:
                    count_sales_today += 1
                    summ_sales_today += sales_30_days[i]['priceWithDisc']
                if sales_30_days[i]['date'].split('T')[0] == yesterday_date:
                    count_sales_yesterday += 1
                    summ_sales_yesterday += sales_30_days[i]['priceWithDisc']
                if sales_30_days[i]['date'].split('T')[0] in week_ago_dates:
                    count_sales_7_days_ago += 1
                    summ_sales_7_days_ago += sales_30_days[i]['priceWithDisc']
                count_sales_3_month += 1
                summ_sales_3_month += sales_30_days[i]['priceWithDisc']
                txt_vrem_hraniliche += f'S_{sales_30_days[i]["date"].split("T")[0]}_{sales_30_days[i]["nmId"]}_{sales_30_days[i]["subject"]}_{sales_30_days[i]["category"]}_{sales_30_days[i]["regionName"]}_{sales_30_days[i]["brand"]}_{sales_30_days[i]["priceWithDisc"]}_{sales_30_days[i]["srid"]}_{sales_30_days[i]["warehouseName"]},'

            if sales_30_days[i]['saleID'][0] == 'R' or 'Возврат' in sales_30_days[i]['orderType'] or 'возврат' in \
                    sales_30_days[i]['orderType']:
                if sales_30_days[i]['lastChangeDate'].split('T')[0] == today_date:
                    count_canceled_today += 1
                    summ_canceled_today += sales_30_days[i]['priceWithDisc']
                if sales_30_days[i]['lastChangeDate'].split('T')[0] == yesterday_date:
                    count_canceled_yesterday += 1
                    summ_canceled_yesterday += sales_30_days[i]['priceWithDisc']
                if sales_30_days[i]['lastChangeDate'].split('T')[0] in week_ago_dates:
                    count_canceled_7_days_ago += 1
                    summ_canceled_7_days_ago += sales_30_days[i]['priceWithDisc']
                count_canceled_3_month += 1
                summ_canceled_3_nomth += sales_30_days[i]['priceWithDisc']
                txt_vrem_hraniliche += f'R_{sales_30_days[i]["date"].split("T")[0]}_{sales_30_days[i]["nmId"]}_{sales_30_days[i]["subject"]}_{sales_30_days[i]["category"]}_{sales_30_days[i]["regionName"]}_{sales_30_days[i]["brand"]}_{sales_30_days[i]["priceWithDisc"]}_{sales_30_days[i]["srid"]}_{sales_30_days[i]["warehouseName"]},'

        txt_vrem_hraniliche += f'|{ip_name}'

        msg = f'СВОДКА\n\n{ip_name}\n\nСЕГОДНЯ\n' \
              f'🛒 Заказы:        {count_orders_today} на {int(summ_orders_today)}₽\n' \
              f'💳 Выкупы:       {count_sales_today} на {int(summ_sales_today)}₽\n' \
              f'↩️ Возвраты:    {count_canceled_today} на {int(summ_canceled_today)}₽\n\n' \
              f'ВЧЕРА\n' \
              f'🛒 Заказы:        {count_orders_yesterday} на {int(summ_orders_yesterday)}₽\n' \
              f'💳 Выкупы:       {count_sales_yesterday} на {int(summ_sales_yesterday)}₽\n' \
              f'↩️ Возвраты:    {count_canceled_yesterday} на {int(summ_canceled_yesterday)}₽\n\n' \
              f'ЗА 7 ДНЕЙ\n' \
              f'🛒 Заказы:        {count_orders_7_days_ago} на {int(summ_orders_7_days_ago)}₽\n' \
              f'💳 Выкупы:       {count_sales_7_days_ago} на {int(summ_sales_7_days_ago)}₽\n' \
              f'↩️ Возвраты:    {count_canceled_7_days_ago} на {int(summ_canceled_7_days_ago)}₽\n\n' \
              f'ЗА 30 ДНЕЙ\n' \
              f'🛒 Заказы:        {count_orders_3_month} на {int(summ_orders_3_month)}₽\n' \
              f'💳 Выкупы:       {count_sales_3_month} на {int(summ_sales_3_month)}₽\n' \
              f'↩️ Возвраты:    {count_canceled_3_month} на {int(summ_canceled_3_nomth)}₽'

        return msg
