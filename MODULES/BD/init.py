import os
import sqlite3
import time
from datetime import datetime

from telebot import types

from MODULES.BOT.init import bot

conn = None
cursor = None


def db_conn_init():
    global cursor, conn
    print(f" > CONNECTING TO DB ......... ", end="")
    try:
        conn = sqlite3.connect("DATA/Dbase.db3", check_same_thread=False)
        print("DONE")
    except Exception as Except_:
        print("NO\n"
              "\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))
        exit()

    print(f" > CREATING DB CURSOR ....... ", end="")
    try:
        cursor = conn.cursor()
        print("DONE")
    except Exception as Except_:
        print("NO\n"
              "\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))
        exit()


def progress(remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')


def backup():
    SCR = f'backup/'

    if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
        path = os.path.join(os.getcwd(), SCR)
        os.mkdir(path)
    con = sqlite3.connect('../../DATA/Dbase.db3')
    bck = sqlite3.connect(f'../../DATA/backup/backup.db3')
    with bck:
        con.backup(bck, pages=1)
    bck.close()
    con.close()


def PREP_BACKUP(message):
    global conn, cursor
    print("    >> backup")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    etap1 = bot.edit_message_text(text="произвожу бекап бд...", chat_id=message.chat.id,
                                  message_id=message.id)

    backup_start_t = time.time()

    cursor.close()
    conn.close()

    backup()

    conn = sqlite3.connect("DATA/Dbase.db3", check_same_thread=False)
    cursor = conn.cursor()

    backup_end_t = time.time()
    bot.delete_message(message.chat.id, etap1.message_id)

    f = open("DATA/backup/backup.db3", "rb")
    bot.send_document(chat_id=message.chat.id, document=f, caption=f"{str(datetime.now()).split('.')[0]}")
    bot.send_message(chat_id=message.chat.id, text=f"Бекап был успешно выполнен за: "
                                                   f"~{round(backup_end_t - backup_start_t, 3)} "
                                                   f"секунды", reply_markup=markup)


def check_user_last_time(message, added_img=False, added_sticker=False):
    global conn, cursor
    ID = message.chat.id
    Name = f"@{message.from_user.username}"
    Now = str(datetime.now()).split(".")[0]

    user = cursor.execute('SELECT * FROM users WHERE ID = ?',
                          (ID,)).fetchall()
    if not user:
        cursor.execute('INSERT INTO users (ID, NAME, LASTTIME, STICKERS, IMAGES) VALUES (?, ?, ?, ?, ?)',
                       (ID, Name, Now, "0", "0"))
    elif user:
        cursor.execute(f'UPDATE users SET LASTTIME = ? WHERE ID = ?',
                       (Now, ID))

    if added_img:
        img_gen = int(user[0][4])
        cursor.execute(f'UPDATE users SET IMAGES = ? WHERE ID = ?',
                       (f"{img_gen + 1}", ID))
    if added_sticker:
        stickers = int(user[0][3])
        cursor.execute(f'UPDATE users SET IMAGES = ? WHERE ID = ?',
                       (f"{stickers + 1}", ID))

    conn.commit()