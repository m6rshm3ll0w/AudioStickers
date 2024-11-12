import time

from MODULES.OTHER.global_init import global_init

global_init()

from MODULES.BOT.ACTIONS.F2A.main import confirm_f2a
from MODULES.BOT.CALLBACK.handler import callback_handler_main
from MODULES.BOT.INLINE.compose import inline_viewer
from MODULES.BOT.OTHER.bot_info import bot_info
from MODULES.BOT.START.hello import start
from MODULES.BOT.STICKERS.ADD.begin import add_sticker
from MODULES.IMGs.gen_img import start_generate_txt2_img
from MODULES.OTHER.global_init import VERSION
from MODULES.BOT.init import bot, poooling_bot


print(f" BOT VERSION {VERSION:^30}")
print(f" STARTING BOT PROCESS: ")

start_time = time.time()

print(f" > INITIALISE ALL BOT FUNC .. ", end="")


@bot.inline_handler(func=lambda query: True)
def handle_inline_query(query):
    inline_viewer(query)


@bot.message_handler(commands=["start"])
def start_command(message):
    start(message)


@bot.callback_query_handler(func=lambda callback: True)
def callback_query_handler(callback):
    callback_handler_main(callback)


@bot.message_handler(content_types=["audio", "voice"])
def adding_sticker(message):
    add_sticker(message)


@bot.message_handler(commands=["generate"])
def generating_image(message):
    start_generate_txt2_img(message)


@bot.message_handler(commands=["F2A"])
def adding_f2a(message):
    confirm_f2a(message)


print("DONE")

bot_info()

end_time = time.time()
print(f"STARTING BOT PROCESS ~{round(float(end_time - start_time), 3)}sec ... ", end="")

poooling_bot()