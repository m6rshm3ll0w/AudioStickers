from datetime import datetime

from MODULES.BOT.init import bot
from MODULES.OTHER.global_init import ADMINS


def bot_info():
    bot_name = str(bot.get_my_name()).split(": ")[1]
    bot_name = bot_name[:len(bot_name) - 2]
    bot_name = bot_name[1:]
    print(
        f'--------------------------------------------\n'
        f' > BOT NAME      : {bot_name}\n'
        f' > BOT ADMINS    : {ADMINS}\n'
        f'--------------------------------------------\n'
        f' > NOW TIME      : {datetime.now()}\n'
        f' > AUTHOR        : @m6rshm3ll0w\n'
        f'--------------------------------------------')