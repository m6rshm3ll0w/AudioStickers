from telebot import types

from MODULES.BD.init import cursor
from MODULES.BOT.STICKERS.ADD.name import sticker_name
from MODULES.BOT.init import bot


def add_sticker(message):
    cursor.execute(f'SELECT ID FROM banlist')
    Banned_USER = cursor.fetchall()
    idu = (f'message.from_user.id',)
    if idu in Banned_USER:
        markup = types.InlineKeyboardMarkup()
        license_text = types.InlineKeyboardButton("УСЛОВИЯ", callback_data="license_text")
        markup.add(license_text)
        back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
        markup.add(back)
        bot.send_message(message.chat.id, "Вы нарушили правила бота, поэтому в оказались в банлисте :(",
                         reply_markup=markup)
    else:
        print(f">>> ADDING A STICKER by @{message.from_user.username}")
        audio = message
        markup = types.InlineKeyboardMarkup()
        license_text = types.InlineKeyboardButton("УСЛОВИЯ", callback_data="license_text")
        markup.add(license_text)
        mmss = bot.send_message(message.chat.id, "Создавая стикер вы принимаете условия\n\n"
                                                 "Придумайте название для стикера....\n"
                                                 "напишите /back если не хотите создавать стикер", reply_markup=markup)
        bot.register_next_step_handler(message, sticker_name, audio, mmss)