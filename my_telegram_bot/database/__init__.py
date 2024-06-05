from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from my_telegram_bot.config import DATABASE

# Формируем URL для подключения к базе данных
DATABASE_URL = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}?client_encoding=utf8"

# Создаем объект engine для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для декларативного определения моделей
Base = declarative_base()