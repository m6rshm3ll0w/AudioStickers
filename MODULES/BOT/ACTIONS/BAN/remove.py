import time

from MODULES.BD.init import cursor, conn
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def UB_U_ID(message, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        IDs = message.text
        cursor.execute(f'DELETE from banlist WHERE ID = ?',
                       f"{IDs}")
        conn.commit()
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id, text=f"{IDs} разбанен")
        bot.send_message(IDs, "Вы разбанены!!!")
        time.sleep(2)
        main_menu(mmss)