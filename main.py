import telebot
from telebot import types
import time
from dotenv import load_dotenv
from db_requests import *
from wb_requests import *

load_dotenv()

bot_token = os.getenv('TOKEN')
bot = telebot.TeleBot(bot_token)

db_query = DbRequest()
api_query = ApiRequest()

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

    reg = False
    for user in all_users:
        if str(message.from_user.id) == user[0]:
            reg = True

    if reg:
        api_key = message.text
        orders_today = api_query.get_orders(api_key, 'today')
        msg, fl_orders_today = check_request(orders_today)
        if fl_orders_today:
            ip_name = api_query.api_ip(225816980, api_key)
            bot.send_message(message.chat.id, ip_name)


bot.polling(non_stop=True, interval=0)
