from telebot import types

from MODULES.BD.init import cursor
from MODULES.BOT.init import bot


def ADM_LIST(message):
    print("    >> loading a viewer")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    cursor.execute('SELECT * FROM admins')
    admins = cursor.fetchall()
    result = "Все админы:\n"

    if len(admins) == 0:
        result = result + "пока тут пусто\n"

    for admuser in admins:
        f = (f"ID {admuser[0]}\n"
             f"NAME {admuser[1]}\n"
             f"> date : {admuser[2]}\n"
             f"> F2A  : {admuser[5]} \n\n")
        result = result + f
    bot.edit_message_text(text=result, chat_id=message.chat.id, message_id=message.id, reply_markup=markup)