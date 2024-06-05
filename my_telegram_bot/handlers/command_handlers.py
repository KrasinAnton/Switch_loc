from telebot import types
from my_telegram_bot.database.db_helper import add_feedback
from my_telegram_bot.utils.user_check import is_allowed_user
from my_telegram_bot.utils.image import send_image
from my_telegram_bot.utils.log import log_activity


# Функция для отправки приветственного сообщения
def send_welcome(bot, message):
    print(f"Команда /start от пользователя: {message.from_user.username}")  # Отладочное сообщение

    # Проверяем, имеет ли пользователь доступ к боту
    if is_allowed_user(message.from_user.username):
        log_activity(message.from_user.username, 'Начал взаимодействие с ботом')  # Логируем начало взаимодействия
        send_image(message.chat.id, bot)  # Отправляем изображение

        # Создаем разметку для inline-клавиатуры с опциями
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton('Где плинты', callback_data='find_plinth')
        item2 = types.InlineKeyboardButton('Добавить адрес', callback_data='add_address')
        markup.add(item1, item2)

        # Отправляем сообщение с просьбой выбрать действие с inline-клавиатурой
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    else:
        # Если пользователь не имеет доступа, отправляем соответствующее сообщение
        bot.reply_to(message, "Вы не имеете доступа к этому боту.")


# Функция для обработки команды фидбэк
def feedback(bot, message):
    print(f"Команда /feedback от пользователя: {message.from_user.username}")  # Отладочное сообщение

    # Проверяем, имеет ли пользователь доступ к боту
    if is_allowed_user(message.from_user.username):
        log_activity(message.from_user.username, 'Запросил фидбэк')  # Логируем запрос фидбэка

        # Создаем разметку для inline-клавиатуры с опцией возврата на главную
        markup = types.InlineKeyboardMarkup()
        item_main = types.InlineKeyboardButton('На главную', callback_data='main')
        markup.add(item_main)

        # Отправляем сообщение с просьбой оставить фидбэк и регистрируем обработчик следующего шага
        bot.send_message(message.chat.id, "Готов записать Ваши пожелания:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: handle_feedback(bot, msg))
    else:
        # Если пользователь не имеет доступа, отправляем соответствующее сообщение
        bot.reply_to(message, "Вы не имеете доступа к этому боту.")


# Функция для обработки текста фидбэка
def handle_feedback(bot, message):
    feedback_text = message.text
    add_feedback(message.from_user.username, feedback_text)  # Сохраняем фидбэк в базу данных

    # Создаем разметку для inline-клавиатуры с опцией возврата на главную
    markup = types.InlineKeyboardMarkup()
    item_main = types.InlineKeyboardButton('На главную', callback_data='main')
    markup.add(item_main)

    # Отправляем сообщение с благодарностью за фидбэк
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!", reply_markup=markup)


# Функция для регистрации обработчиков команд
def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        send_welcome(bot, message)  # Обработчик команды /start

    @bot.message_handler(commands=['feedback'])
    def feedback_command(message):
        feedback(bot, message)  # Обработчик команды /feedback


# Функция для обработки команд
def handle_command(bot, message):
    command = message.text.lower()

    # Определяем действие в зависимости от команды
    if command == '/start':
        send_welcome(bot, message)
    elif command == '/feedback':
        feedback(bot, message)
    else:
        # Если команда неизвестна, отправляем соответствующее сообщение
        bot.reply_to(message, "Я не понимаю эту команду. Попробуй /start.")