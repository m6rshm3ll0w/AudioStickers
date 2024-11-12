import time
from datetime import datetime

import telebot


bot: telebot.TeleBot = None


def bot_init(KEY):
    global bot
    print(f" > INITIALISE BOT ........... ", end="")
    try:
        bot = telebot.TeleBot(KEY)
        print("DONE")
    except Exception as Except_:
        print("NO\n"
              "\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))
        exit()


def poooling_bot():
    while True:
        try:
            print("DONE")
            bot.polling(none_stop=True, interval=0)
            print("\n\nSTOPPING BOT ........ ", end="")
            print("DONE")
            break
        except Exception as Except_:

            print("\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))

            print("RESTARTING...", end="")
            bot.stop_polling()

            time.sleep(10)

            print("DONE\n\n>>>")