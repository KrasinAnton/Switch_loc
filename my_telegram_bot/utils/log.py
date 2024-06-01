from my_telegram_bot.database.db_helper import log_activity_to_db
from datetime import datetime

def log_activity(username, action):
    actions_to_log = [
        'Добавление нового адреса',
        'Добавил новую информацию',
        'Добавил дополнительную информацию',
        'Обновил информацию',
        'Недопустимый пользователь'
    ]
    if any(action.startswith(a) for a in actions_to_log):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_activity_to_db(timestamp, username, action, feedback=None)
