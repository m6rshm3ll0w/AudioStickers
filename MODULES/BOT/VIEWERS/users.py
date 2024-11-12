from telebot import types

from MODULES.BD.init import check_user_last_time, cursor
from MODULES.BOT.init import bot


def USR_LIST(message):
    print("    >> loading a viewer")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    result = "Все пользователи:\n"

    if len(users) == 0:
        result = result + "пока тут пусто\n"

    for user in users:
        f = (f"ID [{user[0]}](tg://user?id={user[0]})\n"
             f"NAME {user[1]}\n"
             f"> last_login : {user[2]}\n"
             f"> s: {user[3]} i: {user[4]}\n\n")
        result = result + f
    bot.edit_message_text(text=result, chat_id=message.chat.id, message_id=message.id, reply_markup=markup,
                          parse_mode="Markdown")