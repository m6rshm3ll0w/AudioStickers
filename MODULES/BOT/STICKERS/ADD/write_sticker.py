import os
import time
import uuid

from telebot import types

from MODULES.BD.init import cursor, conn, check_user_last_time
from MODULES.BOT.START.hello import start
from MODULES.BOT.init import bot


def add_sticker2(message, NAME, audio, BY, DESCRIPTION, TAGS, mmss):
    if message.text == "Все правильно":
        try:
            file_info = bot.get_file(audio.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
        except AttributeError:
            file_info = bot.get_file(audio.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

        SCR = f'converted/'

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, mmss.message_id)

        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        SCR = f"converted/to_voice_last.mp3"

        with open(SCR, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        voice = bot.send_voice(message.chat.id, open(SCR, "rb"))


        file_info = bot.get_file(voice.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        FID = str(uuid.uuid4())
        SCR = f'audio/@{BY}'
        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        SCR = f"{SCR}/{FID}.wav"

        with open(SCR, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        if len(DESCRIPTION) > 43:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(SCR, 'rb'),
                                 title=f"{NAME}",
                                 performer=f"{DESCRIPTION[:len(DESCRIPTION) - 43]}\n{DESCRIPTION[43:]}")
        else:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(SCR, 'rb'),
                                 title=f"{NAME}",
                                 performer=f"{DESCRIPTION}")
        cursor.execute('INSERT INTO audio (NAME, FILE_ID, DESCRIPTION, TAGS) VALUES (?, ?, ?, ?)',
                       (NAME, fid.voice.file_id, DESCRIPTION, TAGS))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("в главное меню 👌", callback_data="del_msg")
        markup.add(back)

        bot.delete_message(message.chat.id, audio.message_id)

        bot.delete_message(message.chat.id, fid.message_id)

        bot.send_message(message.chat.id, "Отлично, стикер добавлен!!!\n"
                                          f"Data:\n"
                                          f"   -name  :{NAME}\n"
                                          f"   -by    :{BY}\n"
                                          f"   -desc. :{DESCRIPTION}", reply_markup=markup)
        check_user_last_time(message, added_sticker=True)

        print(f"            > STICKER ADDED SUCCESSFUL")
    else:
        bot.delete_message(message.chat.id, audio.message_id)

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, mmss.message_id)

        bot.send_message(message.chat.id, "Создание стикера отменено!!!")
        time.sleep(2)
        start(message)