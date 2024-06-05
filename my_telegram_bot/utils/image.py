import os


# Функция для отправки изображения
def send_image(chat_id, bot):
    # Путь к файлу изображения
    image_path = r"D:\UrFU\Items\2_course\2_semestr\Sovr_yazuki_program\pythonProject\Switch_loc\my_telegram_bot\Files\We1a.mp4"

    # Проверяем, существует ли файл по указанному пути
    if os.path.exists(image_path):
        # Открываем файл в режиме чтения байтов и отправляем его
        with open(image_path, 'rb') as image:
            msg = bot.send_photo(chat_id, image)
            return msg
    else:
        # Если файл не найден, выводим сообщение в консоль
        print("File not found!")
        return None