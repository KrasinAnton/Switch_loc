import time
import telebot
from my_telegram_bot.handlers import callback_handlers, command_handlers
from my_telegram_bot.config import TOKEN
import os
import sys
from my_telegram_bot.handlers import message_handlers


bot = telebot.TeleBot(TOKEN)



# Добавление текущего каталога в путь поиска Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Register command handlers
command_handlers.register_handlers(bot)

# Register callback query handlers
callback_handlers.register_handlers(bot)

# Register message handlers
message_handlers.register_handlers(bot)

def start_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Подождите некоторое время перед повторным запуском

if __name__ == '__main__':
    start_polling()