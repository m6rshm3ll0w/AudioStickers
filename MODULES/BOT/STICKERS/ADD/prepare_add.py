from telebot import types

from MODULES.BOT.STICKERS.ADD.write_sticker import add_sticker2
from MODULES.BOT.init import bot


def sticker_to_base(message, audio, NAME, TAGS, ANNONIM, mmss):
    if ANNONIM:
        BY = "$n#ni&"
    else:
        BY = f"{message.from_user.username}"

    if message.text == "/empty":
        DESCRIPTION = f"@{BY} ● мемы"
        print(f"          > descr. SKIPPED >")
    else:
        DESCRIPTION = f"@{BY} ● {message.text}"
        print(f"          > DESCR. : {DESCRIPTION}")

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, mmss.message_id)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    nona = types.KeyboardButton("Все правильно")
    anon = types.KeyboardButton("Нет, вернуться в главное меню")
    markup.add(nona)
    markup.add(anon)

    mmss = bot.send_message(message.chat.id, "Все правильно?\n"
                                             f"Data:\n"
                                             f"   -name  :{NAME}\n"
                                             f"   -by    :{BY}\n"
                                             f"   -desc. :{DESCRIPTION}", reply_markup=markup)
    bot.register_next_step_handler(message, add_sticker2, NAME, audio, BY, DESCRIPTION, TAGS, mmss)