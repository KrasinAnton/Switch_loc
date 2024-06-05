from telebot import types
from threading import Lock
from my_telegram_bot.utils.image import send_image
from my_telegram_bot.utils.log import log_activity
from my_telegram_bot.utils.user_check import is_allowed_user
from my_telegram_bot.database.db_helper import get_address, add_address, update_address_info

# Создаем объект lock для обеспечения потокобезопасности
lock = Lock()


# Функция для запроса у пользователя ввода адреса
def prompt_for_address(chat_id, next_step_handler, bot):
    # Создаем разметку для inline-клавиатуры с кнопкой отмены
    markup = types.InlineKeyboardMarkup()
    item_cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    markup.add(item_cancel)

    # Отправляем сообщение с запросом адреса и inline-клавиатурой
    bot.send_message(chat_id, "Введи адрес:", reply_markup=markup)

    # Регистрируем обработчик следующего шага для ожидания ответа пользователя
    wait_for_address_response(chat_id, next_step_handler, bot)


# Функция для ожидания ответа пользователя с адресом
def wait_for_address_response(chat_id, next_step_handler, bot):
    # Определяем обернутый обработчик для обработки ответа пользователя
    def wrapped_handler(message):
        from my_telegram_bot.handlers.command_handlers import handle_command

        # Если пользователь отправляет команду, обрабатываем ее соответственно
        if message.text.startswith('/'):
            handle_command(bot, message)
            return

        # Вызываем обработчик следующего шага с сообщением пользователя
        next_step_handler(bot, message)

    # Регистрируем обернутый обработчик для следующего шага по ID чата
    bot.register_next_step_handler_by_chat_id(chat_id, wrapped_handler)


# Функция для отправки приветственного сообщения по ID чата
def send_welcome_by_chat_id(chat_id, bot):
    # Отправляем изображение пользователю
    send_image(chat_id, bot)

    # Создаем разметку для inline-клавиатуры с опциями
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Где плинты', callback_data='find_plinth')
    item2 = types.InlineKeyboardButton('Добавить адрес', callback_data='add_address')
    markup.add(item1, item2)

    # Отправляем сообщение с просьбой выбрать действие с inline-клавиатурой
    bot.send_message(chat_id, "Выбери действие:", reply_markup=markup)


# Функция для поиска плинта по адресу
def find_plinth(bot, message):
    address = message.text

    # Проверяем, начинается ли адрес с заглавной буквы
    if not address[0].isupper():
        bot.reply_to(message, "Адрес должен начинаться с заглавной буквы! Введи адрес снова:")
        wait_for_address_response(message.chat.id, find_plinth, bot)
        return

    # Захватываем lock для обеспечения потокобезопасности при доступе к базе данных
    with lock:
        existing_address = get_address(address)

    # Если адрес существует, отправляем информацию пользователю
    if existing_address:
        info = existing_address.info
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, f"Информация по адресу '{address}': {info}", reply_markup=markup)
    else:
        # Если адрес не существует, информируем пользователя
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, f"Информация по адресу '{address}' не найдена.", reply_markup=markup)


# Функция для обработки добавления нового адреса
def add_address_handler(bot, message):
    address = message.text

    # Проверяем, начинается ли адрес с заглавной буквы
    if not address[0].isupper():
        bot.reply_to(message, "Адрес должен начинаться с заглавной буквы! Введи адрес снова:")
        wait_for_address_response(message.chat.id, add_address_handler, bot)
        return

    # Логируем действие по добавлению нового адреса
    log_activity(message.from_user.username, f'Добавление нового адреса {address}')

    # Захватываем lock для обеспечения потокобезопасности при доступе к базе данных
    with lock:
        existing_address = get_address(address)

    # Если адрес уже существует, предоставляем опции для обновления или добавления информации
    if existing_address:
        info = existing_address.info
        markup = types.InlineKeyboardMarkup()
        item_update_info = types.InlineKeyboardButton('Изменить', callback_data=f'update_info:{address}')
        item_add_info = types.InlineKeyboardButton('Добавить', callback_data=f'add_info:{address}')
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_update_info, item_add_info, item_main)
        bot.reply_to(message, f"Адрес '{address}' уже существует с информацией: {info}. Выберите действие:",
                     reply_markup=markup)
    else:
        # Если адрес новый, просим пользователя предоставить информацию для него
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.reply_to(message, "Введите информацию для нового адреса:")
        bot.register_next_step_handler(message, lambda msg: add_info_to_new_address(bot, msg, address))


# Функция для добавления информации к новому адресу
def add_info_to_new_address(bot, message, address):
    info = message.text

    # Логируем действие по добавлению новой информации для адреса
    log_activity(message.from_user.username, f'Добавил новую информацию "{info}" для адреса {address}')

    # Добавляем новый адрес с информацией в базу данных
    add_address(address, info)
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Адрес '{address}' с информацией '{info}' успешно добавлен.", reply_markup=markup)


# Функция для добавления информации к существующему адресу
def append_info(bot, message, address):
    additional_info = message.text

    # Получаем существующую информацию для адреса
    existing_info = get_address(address).info
    new_info = f"{existing_info} {additional_info}"

    # Логируем действие по добавлению дополнительной информации для адреса
    log_activity(message.from_user.username,
                 f'Добавил дополнительную информацию "{additional_info}" для адреса {address}')

    # Обновляем информацию об адресе в базе данных
    update_address_info(address, new_info)
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Информация для адреса '{address}' успешно обновлена. Новая информация: {new_info}",
                 reply_markup=markup)


# Функция для обновления информации для существующего адреса
def update_info(bot, message, address):
    new_info = message.text

    # Логируем действие по обновлению информации для адреса
    log_activity(message.from_user.username, f'Обновил информацию на "{new_info}" для адреса {address}')

    # Обновляем информацию об адресе в базе данных
    update_address_info(address, new_info)
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.reply_to(message, f"Информация для адреса '{address}' успешно обновлена на '{new_info}'.", reply_markup=markup)


# Функция для регистрации обработчиков callback-запросов
def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        try:
            # Проверяем, имеет ли пользователь доступ к боту
            if not is_allowed_user(call.from_user.username):
                log_activity(call.from_user.username, 'Недопустимый пользователь')
                bot.answer_callback_query(call.id, "Вы не имеете доступа к этому боту.")
                return

            # Логируем действие по нажатию кнопки
            log_activity(call.from_user.username, f'Нажата кнопка {call.data}')

            # Обрабатываем различные значения callback data
            if call.data == 'find_plinth':
                bot.answer_callback_query(call.id)
                prompt_for_address(call.message.chat.id, find_plinth, bot)
            elif call.data == 'add_address':
                bot.answer_callback_query(call.id)
                prompt_for_address(call.message.chat.id, add_address_handler, bot)
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
            elif call.data == 'main' or call.data == 'cancel':
                # Удаляем предыдущие обработчики шагов и отправляем приветственное сообщение
                bot.clear_step_handler_by_chat_id(call.message.chat.id)
                bot.answer_callback_query(call.id)
                send_welcome_by_chat_id(call.message.chat.id, bot)
            else:
                bot.answer_callback_query(call.id, "Неизвестная команда.")
        except Exception as e:
            print(f"Error in callback query handler: {e}")
            bot.send_message(call.message.chat.id, "Ошибка! Возврат на главную!")
            send_welcome_by_chat_id(call.message.chat.id, bot)