from sqlalchemy import Column, Integer, String
from . import Base, SessionLocal, engine
from threading import Lock


lock = Lock()

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    info = Column(String, nullable=False)
    added_info = Column(Integer, default=0)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
    username = Column(String, nullable=False)
    action = Column(String, nullable=False)

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

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

def log_activity_to_db(timestamp, username, action):
    with lock:
        session = SessionLocal()
        log_entry = Log(timestamp=timestamp, username=username, action=action)
        session.add(log_entry)
        session.commit()
        session.close()