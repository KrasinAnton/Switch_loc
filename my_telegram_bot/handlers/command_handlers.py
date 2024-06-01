from telebot import types
from my_telegram_bot.database.db_helper import add_feedback
from my_telegram_bot.utils.user_check import is_allowed_user
from my_telegram_bot.utils.image import send_image
from my_telegram_bot.utils.log import log_activity

def send_welcome(bot, message):
    print(f"Команда /start от пользователя: {message.from_user.username}")  # Отладочное сообщение
    if is_allowed_user(message.from_user.username):  # Проверяем доступ только здесь
        log_activity(message.from_user.username, 'Начал взаимодействие с ботом')
        send_image(message.chat.id, bot)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton('Где плинты', callback_data='find_plinth')
        item2 = types.InlineKeyboardButton('Добавить адрес', callback_data='add_address')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    else:
        bot.reply_to(message, "Вы не имеете доступа к этому боту.")

def feedback(bot, message):
    print(f"Команда /feedback от пользователя: {message.from_user.username}")  # Отладочное сообщение
    if is_allowed_user(message.from_user.username):  # Проверяем доступ только здесь
        log_activity(message.from_user.username, 'Запросил фидбэк')
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)
        bot.send_message(message.chat.id, "Готов записать Ваши пожелания:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: handle_feedback(bot, msg))
    else:
        bot.reply_to(message, "Вы не имеете доступа к этому боту.")

def handle_feedback(bot, message):
    feedback_text = message.text
    add_feedback(message.from_user.username, feedback_text)
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!", reply_markup=markup)


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        send_welcome(bot, message)

    @bot.message_handler(commands=['feedback'])
    def feedback_command(message):
        feedback(bot, message)

def handle_command(bot, message):
    command = message.text.lower()
    if command == '/start':
        send_welcome(bot, message)
    elif command == '/feedback':
        feedback(bot, message)
    else:
        bot.reply_to(message, "Я не понимаю эту команду. Попробуй /start.")