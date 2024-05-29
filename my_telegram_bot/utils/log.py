import datetime

def log_activity(username, action):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{current_time} - Пользователь: {username}, Действие: {action}\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_message)