from telebot import types

from MODULES.BD.init import check_user_last_time, cursor
from MODULES.BOT.init import bot

PAGE = 1


def all_s(message):
    check_user_last_time(message)
    print("    >> loading a viewer")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    PAGES = 1
    cursor.execute('SELECT * FROM audio')
    Voices = cursor.fetchall()
    result = "Все аудио стикеры:\n"

    if 1 <= len(Voices) <= 49:
        PAGES = 1
    elif len(Voices) % 49 != 0:
        PAGES = len(Voices) // 49 + 1
    elif len(Voices) % 49 == 0:
        PAGES = len(Voices) // 49
    elif len(Voices) == 0:
        PAGES = 1
        result = result + (" пока тут пусто\n"
                           " добавь свой аудио-стикер!")

    if PAGE == 1 and PAGES != 1:
        left = types.InlineKeyboardButton("<-", callback_data="0")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="page+1")
        markup.add(left, list_p, right)
    elif PAGE == PAGES and PAGES != 1:
        left = types.InlineKeyboardButton("<-", callback_data="page-1")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="0")
        markup.add(left, list_p, right)
    elif 1 < PAGE > PAGES:
        left = types.InlineKeyboardButton("<-", callback_data="page-1")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="page+1")
        markup.add(left, list_p, right)
    else:
        left = types.InlineKeyboardButton("<-", callback_data="0")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="0")
        markup.add(left, list_p, right)

    start_index = 49 * (PAGE - 1)
    end_index = 49 * PAGE
    for x, voice in enumerate(Voices[start_index:end_index], start=start_index):
        f = (f"ID {voice[0]}\n"
             f"NAME    : {voice[1]}\n"
             f"> DESC. : {voice[3]}\n\n")
        result = result + f
    bot.edit_message_text(text=result, chat_id=message.chat.id, message_id=message.id, reply_markup=markup)


def set_page(PAGE_n, plus=False, minus=False):
    global PAGE
    if plus is True:
        PAGE += PAGE_n
    elif minus is True:
        PAGE -= PAGE_n
    else:
        PAGE = PAGE_n