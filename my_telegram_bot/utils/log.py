from my_telegram_bot.database.db_helper import log_activity_to_db
from datetime import datetime


# Функция для логирования активности
def log_activity(username, action):
    # Список действий, которые нужно логировать
    actions_to_log = [
        'Добавление нового адреса',
        'Добавил новую информацию',
        'Добавил дополнительную информацию',
        'Обновил информацию',
        'Недопустимый пользователь'
    ]

    # Проверяем, начинается ли действие с одного из логируемых действий
    if any(action.startswith(a) for a in actions_to_log):
        # Получаем текущую временную метку
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Логируем активность в базу данных
        log_activity_to_db(timestamp, username, action, feedback=None)