from my_telegram_bot.config import ALLOWED_USERNAMES

def is_allowed_user(username):
    print(f"Проверка доступа для пользователя: {username}")  # Отладочное сообщение
    is_allowed = username in ALLOWED_USERNAMES
    print(f"Доступ разрешен: {is_allowed}")  # Отладочное сообщение
    return is_allowed