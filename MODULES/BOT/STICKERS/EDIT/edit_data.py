import os
import time
import uuid

from telebot import types

from MODULES.BD.init import cursor, conn
from MODULES.BOT.START.hello import start
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def E_S_P(message, mmss):
    try:
        print(f"      > edit sticker {message.text}")
        IDs = int(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        e_t = types.KeyboardButton("название")
        e_tags = types.KeyboardButton("теги")
        e_description = types.KeyboardButton("описание")
        e_id = types.KeyboardButton("id")
        mm = types.KeyboardButton("назад")
        markup.add(e_t, e_tags)
        markup.add(e_description, e_id)
        markup.add(mm)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Выбери что изменить ", reply_markup=markup)
        bot.register_next_step_handler(message, E_S_P2, IDs, mmss)
    except ValueError:
        print(f"      > INVALID S_ID")
        mmss = bot.send_message(message.chat.id, "такого id нет....")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        main_menu(message)


def E_S_P2(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(mmss.chat.id, mmss.message_id)
    if str(message.text) == "название":
        print(f"        > NAME")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ На что хочешь изменить название?\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, EN, IDs, mmss)
    if str(message.text) == "теги":
        print(f"        > TAGS")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > tags {str(FILE_id[0][4])}\n"
                                                      f"‖ Введи желаемые теги.\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, ET, IDs, mmss)
    if str(message.text) == "id":
        print(f"        > ID")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > ID {str(FILE_id[0][0])}\n"
                                                      f"‖ Введи желаемый id.\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, EID, IDs, mmss)
    if str(message.text) == "описание":
        print(f"        > DESCRIPTION")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > tags {str(FILE_id[0][4])}\n"
                                                      f"‖ Введи желаемое описание (откуда этот звук).\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, ED, IDs, mmss)
    if str(message.text) == "назад":
        print(f"        < EXITED")
        start(message)


def EN(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW NAME: {message.text}")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()

        try:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)
        except AttributeError:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)

        BY = str(FILE_id[0][3]).split(" ● ")[0]

        FID = str(uuid.uuid4())
        SCR = f'audio/{BY}'
        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        with open(f"{SCR}/{FID}.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        fid = bot.send_audio(message.chat.id,
                             audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                             title=f"{message.text}",
                             performer=f"{FILE_id[0][3]}")
        cursor.execute(f'UPDATE audio SET FILE_ID = ?, NAME = ? WHERE ID = ?',
                       (fid.voice.file_id, message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(3)
        bot.delete_message(fid.chat.id, fid.message_id)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def ET(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW TAGS: {message.text}")
        cursor.execute(f'UPDATE audio SET TAGS = ? WHERE ID = ?',
                       (message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def EID(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW ID: {message.text}")
        cursor.execute(f'UPDATE audio SET ID = ? WHERE ID = ?',
                       (message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def ED(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW DESCR. : {message.text}")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', (IDs,))
        FILE_id = cursor.fetchall()

        try:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)
        except AttributeError:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)

        BY = str(FILE_id[0][3]).split(" ● ")[0]

        FID = str(uuid.uuid4())
        SCR = f'audio/{BY}'
        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        with open(f"{SCR}/{FID}.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        DESCRIPTION = f"{BY} ● {message.text}"
        if len(DESCRIPTION) > 43:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                                 title=f"{FILE_id[0][1]}",
                                 performer=f"{DESCRIPTION[:len(DESCRIPTION) - 43]}\n{DESCRIPTION[43:]}")
        else:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                                 title=f"{FILE_id[0][1]}",
                                 performer=f"{DESCRIPTION}")

        cursor.execute(f'UPDATE audio SET FILE_ID = ?, DESCRIPTION = ? WHERE ID = ?',
                       (fid.voice.file_id, f"{DESCRIPTION}", IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)