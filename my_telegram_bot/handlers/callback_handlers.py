from telebot import types
from threading import Lock
from my_telegram_bot.utils.image import send_image
from my_telegram_bot.utils.log import log_activity
from my_telegram_bot.utils.user_check import is_allowed_user
from my_telegram_bot.database.db_helper import cursor, conn

lock = Lock()

def prompt_for_address(chat_id, next_step_handler, bot):
    markup = types.InlineKeyboardMarkup()
    item_cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    markup.add(item_cancel)
    bot.send_message(chat_id, "Введи адрес:", reply_markup=markup)
    wait_for_address_response(chat_id, next_step_handler, bot)

def wait_for_address_response(chat_id, next_step_handler, bot):
    def wrapped_handler(message):
        from my_telegram_bot.handlers.command_handlers import handle_command
        if message.text.startswith('/'):
            handle_command(bot, message)
            return
        next_step_handler(bot, message)

    bot.register_next_step_handler_by_chat_id(chat_id, wrapped_handler)

def send_welcome_by_chat_id(chat_id, bot):
    send_image(chat_id, bot)
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Где плинты', callback_data='find_plinth')
    item2 = types.InlineKeyboardButton('Добавить адрес', callback_data='add_address')
    markup.add(item1, item2)
    bot.send_message(chat_id, "Выбери действие:", reply_markup=markup)

def find_plinth(bot, message):
    address = message.text
    if not address[0].isupper():
        bot.reply_to(message, "Адрес должен начинаться с прописной буквы! Введи адрес снова:")
        wait_for_address_response(message.chat.id, find_plinth, bot)
        return

    log_activity(message.from_user.username, f'Поиск плинтов по адресу {address}')

    with lock:
        cursor.execute("SELECT * FROM addresses WHERE address=?", (address,))
        existing_address = cursor.fetchone()

    if existing_address:
        info = existing_address[2]
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, f"Информация по адресу '{address}': {info}", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, f"Информация по адресу '{address}' не найдена.", reply_markup=markup)

def add_address(bot, message):
    address = message.text
    if not address[0].isupper():
        bot.reply_to(message, "Адрес должен начинаться с прописной буквы! Введи адрес снова:")
        wait_for_address_response(message.chat.id, add_address, bot)
        return

    log_activity(message.from_user.username, f'Добавление нового адреса {address}')

    with lock:
        cursor.execute("SELECT * FROM addresses WHERE address=?", (address,))
        existing_address = cursor.fetchone()

    if existing_address:
        info = existing_address[2]
        markup = types.InlineKeyboardMarkup()
        item_update_info = types.InlineKeyboardButton('Изменить', callback_data=f'update_info:{address}')
        item_add_info = types.InlineKeyboardButton('Добавить', callback_data=f'add_info:{address}')
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_update_info, item_add_info, item_main)
        bot.reply_to(message, f"Адрес '{address}' уже существует с информацией: {info}. Выберите действие:",
                     reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, "Введите информацию для нового адреса:")
        bot.register_next_step_handler(message, lambda msg: add_info_to_new_address(bot, msg, address))

def add_info_to_new_address(bot, message, address):
    info = message.text
    log_activity(message.from_user.username, f'Добавил новую информацию "{info}" для адреса {address}')
    with lock:
        cursor.execute("INSERT INTO addresses (address, info) VALUES (?, ?)", (address, info))
    conn.commit()
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Адрес '{address}' с информацией '{info}' успешно добавлен.", reply_markup=markup)

def append_info(bot, message, address):
    additional_info = message.text
    with lock:
        cursor.execute("SELECT info FROM addresses WHERE address=?", (address,))
        existing_info = cursor.fetchone()[0]
        new_info = f"{existing_info} {additional_info}"
    log_activity(message.from_user.username, f'Добавил дополнительную информацию "{additional_info}" для адреса {address}')
    with lock:
        cursor.execute("UPDATE addresses SET info = ? WHERE address = ?", (new_info, address))
    conn.commit()
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Информация для адреса '{address}' успешно обновлена. Новая информация: {new_info}",
                 reply_markup=markup)

def update_info(bot, message, address):
    new_info = message.text
    log_activity(message.from_user.username, f'Обновил информацию на "{new_info}" для адреса {address}')
    with lock:
        cursor.execute("UPDATE addresses SET info = ? WHERE address = ?", (new_info, address))
    conn.commit()
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Информация для адреса '{address}' успешно обновлена на '{new_info}'.", reply_markup=markup)

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        try:
            if not is_allowed_user(call.from_user.username):
                bot.answer_callback_query(call.id, "Вы не имеете доступа к этому боту.")
                return

            log_activity(call.from_user.username, f'Нажата кнопка {call.data}')
            if call.data == 'find_plinth':
                bot.answer_callback_query(call.id)
                prompt_for_address(call.message.chat.id, find_plinth, bot)
            elif call.data == 'add_address':
                bot.answer_callback_query(call.id)
                prompt_for_address(call.message.chat.id, add_address, bot)
            elif call.data.startswith('update_info:'):
                address = call.data.split(':')[1]
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, f"Введите новую информацию для адреса '{address}':")
                bot.register_next_step_handler(call.message, lambda msg: update_info(bot, msg, address))
            elif call.data.startswith('add_info:'):
                address = call.data.split(':')[1]
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, f"Введите дополнительную информацию для адреса '{address}':")
                bot.register_next_step_handler(call.message, lambda msg: append_info(bot, msg, address))
            elif call.data == 'main':
                bot.answer_callback_query(call.id)
                send_welcome_by_chat_id(call.message.chat.id, bot)
            elif call.data == 'cancel':
                bot.answer_callback_query(call.id, "Действие отменено.")
                send_welcome_by_chat_id(call.message.chat.id, bot)
            else:
                bot.answer_callback_query(call.id, "Неизвестная команда.")
        except Exception as e:
            print(f"Error in callback query handler: {e}")
            bot.send_message(call.message.chat.id, "Ошибка! Возврат на главную!")
            send_welcome_by_chat_id(call.message.chat.id, bot)