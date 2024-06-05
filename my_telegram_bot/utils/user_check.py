from my_telegram_bot.config import ALLOWED_USERNAMES


# Функция для проверки, имеет ли пользователь доступ
def is_allowed_user(username):
    print(f"Проверка доступа для пользователя: {username}")  # Отладочное сообщение

    # Проверяем, есть ли имя пользователя в списке разрешенных
    is_allowed = username in ALLOWED_USERNAMES

    print(f"Доступ разрешен: {is_allowed}")  # Отладочное сообщение
    return is_allowed