import time
from datetime import datetime

from MODULES.BD.init import cursor, conn
from MODULES.BOT.START.hello import start
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def B_U_ID(message, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:

        print(f"      > del sticker {message.text}")
        try:
            IDs = int(message.text)
            mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                         text="Ты точно хочешь забанить человека, если да то напиши \n"
                                              f" >>> я хочу забанить {IDs}\n"
                                              "/back - вернуться в главное меню")
            bot.register_next_step_handler(message, B_U_ID_2, IDs, mmss)
        except ValueError:
            abc = bot.send_message(message.chat.id, "Нет такого ID")
            time.sleep(2)
            bot.delete_message(abc.chat.id, abc.message_id)
            start(mmss)


def B_U_ID_2(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == f"я хочу забанить {IDs}":
        print(f"        > deleting accepted!")
        cursor.execute("INSERT INTO banlist (ID, DATE) VALUES (?, ?)",
                       (IDs, str(datetime.now())))
        conn.commit()
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id, text=f"{IDs} забанен (")
        time.sleep(2)
        main_menu(mmss)
    else:
        print(f"        < ABORTED")
        main_menu(mmss)