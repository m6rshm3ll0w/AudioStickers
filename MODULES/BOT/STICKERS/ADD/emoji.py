from telebot import types

from MODULES.BOT.STICKERS.ADD.anon import you_anonimus
from MODULES.BOT.init import bot


def sticker_emoji(message, audio, name, mmss):
    if message.text == "/empty":
        print(f"      > emoji SKIPPED >")
        NAME = name
        print(f"      > FULL NAME: {NAME}")
    else:
        EMOJI = message.text
        NAME = EMOJI + " " + name
        print(f"      > EMOJI: {EMOJI}")
        print(f"      > FULL NAME: {NAME}")
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, mmss.message_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    empty = types.KeyboardButton("/empty")
    markup.add(empty)
    mmss = bot.send_message(message.chat.id, "ОК, теперь напиши теги в формате:\n"
                                             "#tag1 #tag2 #tag3...\n", reply_markup=markup)
    bot.register_next_step_handler(message, you_anonimus, audio, NAME, mmss)