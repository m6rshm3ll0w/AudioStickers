from telebot import types

from MODULES.BOT.START.hello import start
from MODULES.BOT.STICKERS.ADD.emoji import sticker_emoji
from MODULES.BOT.init import bot


def sticker_name(message, audio, mmss):
    if message.text == "/back":
        print("<<< ABORTED")
        start(message)
    else:
        name = message.text
        print(f"    > NAME: {name}")
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, mmss.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        empty = types.KeyboardButton("/empty")
        markup.add(empty)
        mmss = bot.send_message(message.chat.id,
                                "ОК, теперь выбери эмодзи для стикера...\n"
                                "если эмодзи нет просто напишите \n/empty", reply_markup=markup)
        bot.register_next_step_handler(message, sticker_emoji, audio, name, mmss)