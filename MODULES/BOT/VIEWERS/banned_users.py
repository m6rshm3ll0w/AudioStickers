from telebot import types

from MODULES.BD.init import cursor
from MODULES.BOT.init import bot


def Ban_LIST(message):
    print("    >> loading a viewer")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    cursor.execute('SELECT * FROM banlist')
    banlist = cursor.fetchall()
    result = "Все забаненные юзеры:\n"

    if len(banlist) == 0:
        result = result + "пока тут пусто\n"

    for banneduser in banlist:
        f = (f"ID {banneduser[0]}\n"
             f"> date. : {banneduser[1]}\n\n")
        result = result + f
    bot.edit_message_text(text=result, chat_id=message.chat.id, message_id=message.id, reply_markup=markup)