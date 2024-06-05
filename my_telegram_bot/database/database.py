import sys
import os

from my_telegram_bot.config import DATABASE

# Добавляем корневую директорию проекта в sys.path, чтобы можно было импортировать config
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Формируем URL для подключения к базе данных с использованием psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}?client_encoding=utf8"

# Создаем объект engine для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для декларативного определения моделей
Base = declarative_base()