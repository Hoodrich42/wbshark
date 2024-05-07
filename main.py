import telebot
from telebot import types
import threading
import time
from notifications import Notifications
from dotenv import load_dotenv
from db_requests import *
from wb_requests import *

load_dotenv()

bot_token = os.getenv('TOKEN')
bot = telebot.TeleBot(bot_token)

db_query = DbRequest()
api_query = ApiRequest()
notifications = Notifications()

def check_request(response):
    fl_api = False
    msg = ''
    try:
        if response['code'] == 400:
            fl_api = False
            msg = "can't parse dateFrom"
        if response['code'] == 429:
            fl_api = False
            msg = "Слишком много запросов"
        if response['code'] == 401:
            fl_api = False
            msg = 'неверный токен'
            return msg, fl_api
    except:
        fl_api = True
    return msg, fl_api

def check_notifications():
    while True:
        all_users = db_query.select_all()
        for user in all_users:
            telegram_id = user[0]
            api_keys_list = user[1].split('|')
            for api_key in api_keys_list:
                api_key_number = api_keys_list.index(api_key)
                response = notifications.order_cheking('cancel', telegram_id, api_key_number, api_key)
                print(len(response))
                #bot.send_message(telegram_id, response)
                time.sleep(100)
        time.sleep(5)


@bot.message_handler(commands=['start'])
def startt(message):
    telegram_id = str(message.from_user.id)
    reg = False
    all_users = db_query.select_all()
    for user in all_users:
        if telegram_id == user[0]:
            reg = True

    if not reg:
        db_query.insert_db(telegram_id)

    start_markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('👉 Подключить бесплатно', callback_data='podkluchenie')
    start_markup.add(btn1)
    msg = f'🦈 WB Shark Bot - создан для эффективного контролирования продаж на WB. Вот его основные функции:\n\n' \
          f'- 🛒 Уведомления о новых заказах\n' \
          f'- ✅ Уведомления о новых выкупах\n' \
          f'- 📦 Остатки на складах\n' \
          f'- 💼 Процент комиссии\n' \
          f'- 🚛 Стоимость логистики и регион покупателя\n' \
          f'- 📑 Сводка по продажам\n\n' \
          f'Особенности бота:\n' \
          f'- 🟩 АВС анализ\n' \
          f'- 🌊 Режим работы Storm: бот работает даже во время сбоев WB и продолжает отправлять информацию о новых заказах и выкупах\n' \
          f'- 👥 Возможность подключения нескольких кабинетов WB\n' \
          f'- 🗃️ Пополнение склада для каждого артикула с выбором периода (7, 14, 30, 60 дней)\n' \
          f'- ❗️Полное отсутствие рекламы'
    bot.send_message(message.chat.id, text=f'{msg}', reply_markup=start_markup)

@bot.message_handler(content_types=['text'])
def add_api_key(message):
    all_users = db_query.select_all()
    telegram_id = message.from_user.id

    reg = False
    for user in all_users:
        if str(telegram_id) == user[0]:
            reg = True

    if reg:
        api_key = message.text
        orders_today = api_query.get_orders(api_key, 'today')
        msg, fl_orders_today = check_request(orders_today)
        if fl_orders_today:
            nm_id = orders_today[0]['nmId']
            ip_name = api_query.api_ip(nm_id, api_key)
            api_keys_list = db_query.select_api_key(telegram_id).split('|')
            ip_names_list = db_query.select_ip_name(telegram_id).split('|')
            print(api_keys_list)
            if api_keys_list[0] == 'none' or api_keys_list[1] == 'none':
                confirm_marup = types.InlineKeyboardMarkup()
                if api_keys_list[0] == 'none':
                    new_api_key = f'{api_key}*|none'
                    new_ip_name = f'{ip_name}*|none'
                elif api_keys_list[1] == 'none':
                    new_api_key = f'{api_keys_list[0]}|{api_key}*'
                    new_ip_name = f'{ip_names_list[0]}|{ip_name}*'
                db_query.update_ip_name(telegram_id, new_ip_name)
                db_query.update_api_key(telegram_id, new_api_key)
                btn1 = types.InlineKeyboardButton('Да', callback_data='confirm_api_key')
                btn2 = types.InlineKeyboardButton('Нет', callback_data='cancel_api_key')
                confirm_marup.add(btn1, btn2)
                bot.send_message(message.chat.id, text=f'{ip_name}\n\nДобавить API ключ?', reply_markup=confirm_marup)
            else:
                bot.send_message(message.chat.id, text=f'У вас уже активировано 2 API ключа')
        else:
            bot.send_message(message.chat.id, text=f'Неудается получить доступ к статистике\n\nПроверьте правильность API ключа или повторите попытку через пару минут')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    data = call.data.split(':')
    telegram_id = call.from_user.id
    if data[0] == 'confirm_api_key':
        api_keys_list = db_query.select_api_key(telegram_id).split('|')
        ip_names_list = db_query.select_ip_name(telegram_id).split('|')
        if '*' in api_keys_list[0]:
            api_keys_list[0] = api_keys_list[0].split('*')[0]
            ip_names_list[0] = ip_names_list[0].split('*')[0]
        elif '*' in api_keys_list[1]:
            api_keys_list[1] = api_keys_list[1].split('*')[0]
            ip_names_list[1] = ip_names_list[1].split('*')[0]
        db_query.update_api_key(telegram_id, f'{api_keys_list[0]}|{api_keys_list[1]}')
        db_query.update_ip_name(telegram_id, f'{ip_names_list[0]}|{ip_names_list[1]}')
        msg = '✅ Вы успешно подключились!\n\n' \
              '🕒 Как только появится новый заказ, WB Order Bot соберет статистику и пришлет уведомление.'
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id)

    if data[0] == 'cancel_api_key':
        api_keys_list = db_query.select_api_key(telegram_id).split('|')
        ip_names_list = db_query.select_ip_name(telegram_id).split('|')
        if '*' in api_keys_list[0]:
            api_keys_list[0] = 'none'
            ip_names_list[0] = 'none'
        elif '*' in api_keys_list[1]:
            api_keys_list[1] = 'none'
            ip_names_list[1] = 'none'
        db_query.update_api_key(telegram_id, f'{api_keys_list[0]}|{api_keys_list[1]}')
        db_query.update_ip_name(telegram_id, f'{ip_names_list[0]}|{ip_names_list[1]}')
        bot.edit_message_text('Запрос отменен', call.message.chat.id, call.message.message_id)

thread1 = threading.Thread(target=check_notifications).start()
bot.polling(non_stop=True, interval=0)
