from db_requests import DbRequest

db_query = DbRequest()


class Notification:

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

    def order_cheking(self, type, telegram_id, api_key_number):
        if type == 'order':
            today_list = db_query.select_orders_today(telegram_id).split('|')[api_key_number].split(',')
        elif type == 'sale':
            today_list = db_query.select_sales_today(telegram_id).split('|')[api_key_number].split(',')
        elif type == 'cancel':
            today_list = db_query.select_cancel_today(telegram_id).split('|')[api_key_number].split(',')

        return today_list
