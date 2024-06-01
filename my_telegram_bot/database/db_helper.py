from . import SessionLocal
from threading import Lock
from .models import Address, Log, Feedback

lock = Lock()

def get_address(address):
    with lock:
        session = SessionLocal()
        result = session.query(Address).filter(Address.address == address).first()
        session.close()
        return result

def add_address(address, info):
    with lock:
        session = SessionLocal()
        new_address = Address(address=address, info=info)
        session.add(new_address)
        session.commit()
        session.close()

def update_address_info(address, info):
    with lock:
        session = SessionLocal()
        address_record = session.query(Address).filter(Address.address == address).first()
        if address_record:
            address_record.info = info
            session.commit()
        session.close()

def log_activity_to_db(timestamp, username, action, feedback=None):
    with lock:
        session = SessionLocal()
        log_entry = Log(timestamp=timestamp, username=username, action=action, feedback=feedback)
        session.add(log_entry)
        session.commit()
        session.close()

def add_feedback(username, text):
    with lock:
        session = SessionLocal()
        feedback_entry = Feedback(username=username, text=text)
        session.add(feedback_entry)
        session.commit()
        session.close()