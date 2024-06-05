from . import SessionLocal
from threading import Lock
from .models import Address, Log, Feedback

# Создаем объект lock для обеспечения потокобезопасности
lock = Lock()

# Функция для получения адреса из базы данных
def get_address(address):
    with lock:
        session = SessionLocal()  # Создаем сессию
        result = session.query(Address).filter(Address.address == address).first()  # Запрос в базу данных
        session.close()  # Закрываем сессию
        return result

# Функция для добавления нового адреса в базу данных
def add_address(address, info):
    with lock:
        session = SessionLocal()  # Создаем сессию
        new_address = Address(address=address, info=info)  # Создаем новый объект Address
        session.add(new_address)  # Добавляем его в сессию
        session.commit()  # Фиксируем изменения
        session.close()  # Закрываем сессию

# Функция для обновления информации об адресе в базе данных
def update_address_info(address, info):
    with lock:
        session = SessionLocal()  # Создаем сессию
        address_record = session.query(Address).filter(Address.address == address).first()  # Запрос в базу данных
        if address_record:
            address_record.info = info  # Обновляем информацию
            session.commit()  # Фиксируем изменения
        session.close()  # Закрываем сессию

# Функция для логирования активности в базе данных
def log_activity_to_db(timestamp, username, action, feedback=None):
    with lock:
        session = SessionLocal()  # Создаем сессию
        log_entry = Log(timestamp=timestamp, username=username, action=action, feedback=feedback)  # Создаем новый объект Log
        session.add(log_entry)  # Добавляем его в сессию
        session.commit()  # Фиксируем изменения
        session.close()  # Закрываем сессию

# Функция для добавления отзыва в базу данных
def add_feedback(username, text):
    with lock:
        session = SessionLocal()  # Создаем сессию
        feedback_entry = Feedback(username=username, text=text)  # Создаем новый объект Feedback
        session.add(feedback_entry)  # Добавляем его в сессию
        session.commit()  # Фиксируем изменения
        session.close()  # Закрываем сессию