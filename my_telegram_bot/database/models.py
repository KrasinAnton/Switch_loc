from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from datetime import datetime

from my_telegram_bot.config import DATABASE

# Формируем URL для подключения к базе данных с использованием psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}?client_encoding=utf8"

# Создаем объект engine для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для декларативного определения моделей
Base = declarative_base()

# Определение модели Address
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    info = Column(String, nullable=False)
    added_info = Column(Integer, default=0)

# Определение модели Log
class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
    username = Column(String, nullable=False)
    action = Column(String, nullable=False)
    feedback = Column(String, nullable=True)

# Определение модели Feedback
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    username = Column(String, nullable=False)
    text = Column(String, nullable=False)

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Проверка существования таблицы 'feedback'
inspector = inspect(engine)
if not inspector.has_table('feedback'):
    Feedback.__table__.create(bind=engine)