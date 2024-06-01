import datetime
from my_telegram_bot.database.db_helper import log_activity_to_db

def log_activity(username, action):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_activity_to_db(current_time, username, action)