# Импортируем модуль time для работы с задержками
import time
# Импортируем библиотеку telebot для создания Telegram-ботов
import telebot
# Импортируем модули с обработчиками команд, callback-запросов и сообщений
from my_telegram_bot.handlers import callback_handlers, command_handlers
from my_telegram_bot.config import TOKEN  # Импортируем токен для авторизации бота
import os  # Импортируем модуль os для работы с файловой системой
import sys  # Импортируем модуль sys для работы с системными путями
from my_telegram_bot.handlers import message_handlers  # Импортируем обработчик сообщений

# Создаем экземпляр бота с использованием токена
bot = telebot.TeleBot(TOKEN)

# Добавление текущего каталога в путь поиска Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Регистрируем обработчики команд
command_handlers.register_handlers(bot)

# Регистрируем обработчики callback-запросов
callback_handlers.register_handlers(bot)

# Регистрируем обработчики сообщений
message_handlers.register_handlers(bot)

# Функция для запуска бота в бесконечном цикле
def start_polling():
    while True:
        try:
            # Запускаем бот в режиме polling (ожидание входящих сообщений)
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            # Если произошла ошибка, выводим ее в консоль
            print(f"Error: {e}")
            # Ждем 5 секунд перед перезапуском бота
            time.sleep(5)

# Точка входа в программу
if __name__ == '__main__':
    start_polling()