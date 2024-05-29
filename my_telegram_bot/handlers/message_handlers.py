from .command_handlers import handle_command

def register_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        if message.text.startswith('/'):
            handle_command(bot, message)
        else:
            bot.reply_to(message, "Я понимаю только команды, начинающиеся с символа '/'.")