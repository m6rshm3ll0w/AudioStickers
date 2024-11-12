from telebot import types

from MODULES.BOT.STICKERS.ADD.decription import sticker_description
from MODULES.BOT.init import bot


def you_anonimus(message, audio, NAME, mmss):
    if message.text == "/empty":
        TAGS = "#пусто"
        print(f"        > tag SKIPPED >")
    else:
        TAGS = message.text
        print(f"        > TAGS: {TAGS}")

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, mmss.message_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    nona = types.KeyboardButton("показывать мой ник")
    anon = types.KeyboardButton("скрыть мой ник")
    markup.add(nona)
    markup.add(anon)
    mmss = bot.send_message(message.chat.id, "ОК, теперь реши, остаться анонимным или показать что"
                                             " этот стикер добавил ты???", reply_markup=markup)
    bot.register_next_step_handler(message, sticker_description, audio, NAME, TAGS, mmss)