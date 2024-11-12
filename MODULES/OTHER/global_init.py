import sys

from dotenv import dotenv_values

from MODULES.BD.init import db_conn_init
from MODULES.BOT.init import bot_init
from MODULES.GROQ.init import groq_init
from MODULES.IMGs.init import fusion_init


loc_s = dotenv_values("DATA/.env")
try:

    VERSION = loc_s["version"]
    BOT_KEY = loc_s["bot-key"]
    GROQ_KEY = loc_s["groq-key"]
    FUSION_KEY = loc_s["fusion-key"]
    FUSION_SECRET = loc_s["fusion-secret"]
    ChatGPT = loc_s["ChatGPT"]
    Search_icon = loc_s["Search_icon"]
    Chatgpt_ICON = loc_s["Chatgpt_ICON"]
    code_by = loc_s["BY"]
    audio_by = loc_s["AUDIO"]
    ADMINS = loc_s["ADMINS"].split(", ")

except Exception as e:
    print("""
####################################
#        ERROR in .env
#               ^^^^^^
#        Please set .env vars using .env.example
####################################
""")
    print(f"NOT SET: {e}")
    sys.exit()


def global_init():

    bot_init(BOT_KEY)

    groq_init(GROQ_KEY)

    fusion_init(FUSION_KEY, FUSION_SECRET)

    db_conn_init()