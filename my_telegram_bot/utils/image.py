import os

def send_image(chat_id, bot):
    image_path = r"D:\UrFU\Items\2_course\2_semestr\Sovr_yazuki_program\pythonProject\Switch_loc\my_telegram_bot\Files\We1a.mp4"
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image:
            msg = bot.send_photo(chat_id, image)
            return msg
    else:
        print("File not found!")
        return None