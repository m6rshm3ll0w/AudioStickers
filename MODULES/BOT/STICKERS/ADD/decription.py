from telebot import types

from MODULES.BOT.STICKERS.ADD.prepare_add import sticker_to_base
from MODULES.BOT.init import bot


def sticker_description(message, audio, NAME, TAGS, mmss):
    if message.text == "скрыть мой ник":
        ANNONIM = True
    else:
        ANNONIM = False
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, mmss.message_id)

    print(f"        > ANNONIM = {ANNONIM}")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    empty = types.KeyboardButton("/empty")
    r18 = types.KeyboardButton("мемы (R18)")
    markup.add(empty)
    markup.add(r18)
    mmss = bot.send_message(message.chat.id, "ОК, теперь напиши описание(откуда этот трек или его настоящий автор):\n"
                                             "!!! если стикер не предназначен для совершеннолетней аудитории допишите "
                                             "(R18)\n"
                            , reply_markup=markup)
    bot.register_next_step_handler(message, sticker_to_base, audio, NAME, TAGS, ANNONIM, mmss)