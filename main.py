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
                if api_key != 'none':
                    api_key_number = api_keys_list.index(api_key)
                    notifications.order_cheking('order', telegram_id, api_key_number, api_key)
                    # notifications.order_cheking('sale', telegram_id, api_key_number, api_key)
                    # notifications.order_cheking('cancel', telegram_id, api_key_number, api_key)
                    #bot.send_message(telegram_id, msg)
                    time.sleep(1)
        time.sleep(3600)


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


@bot.message_handler(commands=['my'])
def kabinet(message):
    kabinet_markup = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton(f'Управление API ключами', callback_data=f'api_keys')
    btn4 = types.InlineKeyboardButton(f'👨🏻‍💻Поддержка', url='https://t.me/dolphey271')
    btn1 = types.InlineKeyboardButton(f'⚙️ Настройки', callback_data='settings')
    #btn2 = types.InlineKeyboardButton(f'💰 Баланс', callback_data=f'balance')
    kabinet_markup.add(btn1).add(btn3).add(btn4)
    ip_name_list = db_query.select_ip_name(message.from_user.id).split('|')
    bot.send_message(message.chat.id, text=f'🐲 Личный кабинет \n\n· ID: {message.from_user.id}\n\n· Магазины: {len(ip_name_list)}', reply_markup=kabinet_markup)


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
                db_query.update_ip_name(new_ip_name, telegram_id)
                db_query.update_api_key(new_api_key, telegram_id)
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
        db_query.update_api_key(f'{api_keys_list[0]}|{api_keys_list[1]}', telegram_id)
        db_query.update_ip_name(f'{ip_names_list[0]}|{ip_names_list[1]}', telegram_id)
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
        db_query.update_api_key(f'{api_keys_list[0]}|{api_keys_list[1]}', telegram_id)
        db_query.update_ip_name(f'{ip_names_list[0]}|{ip_names_list[1]}', telegram_id)
        bot.edit_message_text('Запрос отменен', call.message.chat.id, call.message.message_id)

    if data[0] == 'settings':
        if len(data) > 1:
            rezerv = db_query.select_rezerv(call.from_user.id).split('|')[int(data[1])]
            settings_markup = types.InlineKeyboardMarkup()
            ip_name = db_query.select_ip_name(call.from_user.id).split('|')[int(data[1])]
            btn1 = types.InlineKeyboardButton(f'Резерв склада: {rezerv} дн.', callback_data=f'rezerv:{data[1]}')
            settings_markup.add(btn1)
            bot.edit_message_text(f'⚙️ Настройки\n\n{ip_name}', call.message.chat.id, call.message.message_id, reply_markup=settings_markup)
        else:
            ip_name_list = db_query.select_ip_name(call.from_user.id).split('|')
            cur_ip_markup = types.InlineKeyboardMarkup()
            for i in range(len(ip_name_list)):
                if ip_name_list[i] != 'none':
                    btn = types.InlineKeyboardButton(f'{ip_name_list[i]}', callback_data=f'settings:{i}')
                    cur_ip_markup.add(btn)
            bot.edit_message_text(f'Выберите магазин:', call.message.chat.id, call.message.message_id, reply_markup=cur_ip_markup)

    if data[0] == 'rezerv':
        if len(data) < 3:
            ip_name = db_query.select_ip_name(call.from_user.id).split('|')[int(data[1])]
            rezerv_markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('7 дн.', callback_data=f'rezerv:{data[1]}:7')
            btn2 = types.InlineKeyboardButton('14 дн.', callback_data=f'rezerv:{data[1]}:14')
            btn3 = types.InlineKeyboardButton('30 дн.', callback_data=f'rezerv:{data[1]}:30')
            btn4 = types.InlineKeyboardButton('60 дн.', callback_data=f'rezerv:{data[1]}:60')
            rezerv_markup.add(btn1, btn2).add(btn3, btn4)
            bot.edit_message_text(f'{ip_name}\n\nВыберите количество дней:', call.message.chat.id, call.message.message_id, reply_markup=rezerv_markup)
        else:
            rezerv = db_query.select_rezerv(call.from_user.id).split('|')
            rezerv[int(data[1])] = int(data[2])
            new_rezerv = ''
            for i in range(len(rezerv)):
                if i + 1 == len(rezerv):
                    new_rezerv += f'{rezerv[i]}'
                else:
                    new_rezerv += f'{rezerv[i]}|'
            db_query.update_rezerv(new_rezerv, call.from_user.id)
            bot.edit_message_text(f'Данные успешно обновленны', call.message.chat.id, call.message.message_id)

    if data[0] == 'api_keys':
        ip_names = db_query.select_ip_name(call.from_user.id).split('|')
        api_keys_edit_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(f'Добавить API ключ', callback_data=f'add_api_key')
        if ip_names[0] != 'none':
            msg = ''
            for i in range(len(ip_names)):
                if ip_names[i] != 'none':
                    if i + 1 == len(ip_names):
                        msg += f'{i + 1}. {ip_names[i]}'
                    else:
                        msg += f'{i + 1}. {ip_names[i]}\n'

            btn2 = types.InlineKeyboardButton(f'Удалить API ключ', callback_data=f'delete_api_key')
            if 'none' in ip_names:
                api_keys_edit_markup.add(btn1)
            api_keys_edit_markup.add(btn2)
            bot.edit_message_text(f'{msg}', call.message.chat.id, call.message.message_id,reply_markup=api_keys_edit_markup)
        else:
            api_keys_edit_markup.add(btn1)
            bot.edit_message_text(f'У вас не подключено ни одного API ключа', call.message.chat.id, call.message.message_id, reply_markup=api_keys_edit_markup)

    if data[0] == 'add_api_key':
        bot.edit_message_text('🛠 ПОДКЛЮЧЕНИЕ\n\n1️⃣ Зайдите в Личный кабинет WB → Настройки → Доступ к API (<a href="https://seller.wildberries.ru/supplier-settings/access-to-api">ссылка</a>). \n\n2️⃣ Нажмите кнопку [+ Создать новый токен] и введите любое имя токена. \n\n3️⃣ Нажмите галочку Только на чтение и выберите тип Статистика.\n\n4️⃣ Нажмите [Создать токен], а затем скопируйте его.\n\n📝 Вставьте скопированный токен в сообщение этого чата:', call.message.chat.id, call.message.message_id, parse_mode='html')

    if data[0] == 'delete_api_key':
        api_keys_markup = types.InlineKeyboardMarkup()
        ip_names = db_query.select_ip_name(call.from_user.id).split('|')
        for i in range(len(ip_names)):
            if ip_names[i] != 'none':
                btn1 = types.InlineKeyboardButton(f'{ip_names[i]}', callback_data=f'current_ip:{i}')
                api_keys_markup.add(btn1)
        btn_otmena = types.InlineKeyboardButton(f'Отмена', callback_data=f'otmena_del')
        api_keys_markup.add(btn_otmena)
        bot.edit_message_text(f'Выберите API ключ который хотите удалить', call.message.chat.id, call.message.message_id, reply_markup=api_keys_markup)

    if data[0] == 'current_ip':
        ip_names = db_query.select_ip_name(call.from_user.id).split('|')
        cur_ip_name = int(data[1])
        deleted_ip = ip_names[cur_ip_name]
        ip_names[cur_ip_name] = 'none'
        updated_ip_names = ''
        print(ip_names)
        for i in range(len(ip_names)):
            if i + 1 == len(ip_names):
                updated_ip_names += f'{ip_names[i]}'
            else:
                updated_ip_names += f'{ip_names[i]}|'
        db_query.update_ip_name(updated_ip_names, call.from_user.id)
        api_keys = db_query.select_api_key(call.from_user.id).split('|')
        api_keys[cur_ip_name] = 'none'
        updated_api_keys = ''
        for i in range(len(api_keys)):
            if i + 1 == len(api_keys):
                updated_api_keys += f'{api_keys[i]}'
            else:
                updated_api_keys += f'{api_keys[i]}|'
        db_query.update_api_key(updated_api_keys, call.from_user.id)
        bot.edit_message_text(f'{deleted_ip} успешно удалено', call.message.chat.id, call.message.message_id)

    if data[0] == 'otmena_del':
        bot.edit_message_text(f'Запрос отменен', call.message.chat.id, call.message.message_id)

    if data[0] == 'podkluchenie':
        podkluch_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('👨🏻‍🎓 Подробнее про API', callback_data='podrobneeapi')
        btn2 = types.InlineKeyboardButton('👨🏻‍💻 Поддержка', url='https://t.me/dolphey271')
        btn3 = types.InlineKeyboardButton('⬅️ Назад', callback_data='start')
        podkluch_markup.add(btn1).add(btn2).add(btn3)
        bot.edit_message_text('🛠 ПОДКЛЮЧЕНИЕ\n\n1️⃣ Зайдите в Личный кабинет WB → Настройки → Доступ к API (<a href="https://seller.wildberries.ru/supplier-settings/access-to-api">ссылка</a>). \n\n2️⃣ Нажмите кнопку [+ Создать новый токен] и введите любое имя токена. \n\n3️⃣ Нажмите галочку Только на чтение и выберите тип Статистика.\n\n4️⃣ Нажмите [Создать токен], а затем скопируйте его.\n\n📝 Вставьте скопированный токен в сообщение этого чата:', call.message.chat.id, call.message.message_id, reply_markup=podkluch_markup, parse_mode='html')

    if data[0] == 'podrobneeapi':
        podrob_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('⬅️ Назад', callback_data='podkluchenie')
        podrob_markup.add(btn1)
        bot.edit_message_text('🔑 API токен (ключ) Wildberries\n\nЕсли кратко, то API-токен — это идентификатор поставщика Wildberries, с помощью которого можно получать информацию о заказах, продажах, поступлениях, наличию на складах и другим данным конкретного поставщика, без доступа к личному кабинету. Далее на основе полученной информации можно строить аналитику.\n\nAPI-токен — это способ интегрирования с теми или иными сервисами, которые созданы для того, чтобы помочь поставщикам в работе с Wildberries. \n\nПреимущества API:\n\n✴️ С помощью API вы получаете детализированную информацию по продажам, заказам и поставкам. WB же в большинстве своих отчетов даёт лишь общую информацию. \n\n✴️ API безопасен и даёт возможность только получать данные, это значит, что вероятность изменения или какого-либо влияния на информацию исключена. \n\n✴️ Вы в любой момент можете сгенерировать новый API-токен в личном кабинете WB, а значит отменить доступ к статистическим данным для нашего бота или других сервисов.', call.message.chat.id, call.message.message_id, reply_markup=podrob_markup)


thread1 = threading.Thread(target=check_notifications).start()
bot.polling(non_stop=True, interval=0)
