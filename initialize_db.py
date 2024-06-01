from my_telegram_bot.database import engine, Base

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы.")