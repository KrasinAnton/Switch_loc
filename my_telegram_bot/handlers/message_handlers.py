from .command_handlers import handle_command

# Функция для регистрации обработчиков
def register_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        # Проверяем, начинается ли сообщение с символа '/'
        if message.text.startswith('/'):
            handle_command(bot, message)  # Обрабатываем команду
        else:
            # Если сообщение не является командой, отправляем соответствующее сообщение
            bot.reply_to(message, "Я понимаю только команды, начинающиеся с символа '/'.")