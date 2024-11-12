import time

from MODULES.BD.init import cursor, conn
from MODULES.BOT.START.hello import start
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def D_S(message, mmss):
    print(f"      > del sticker {message.text}")
    bot.delete_message(message.chat.id, message.message_id)
    try:
        IDs = int(message.text)
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                     text="Ты точно хочешь удалить стикер из базы данных, если да то напиши \n"
                                          f" >>> я хочу удалить стикер {IDs}\n"
                                          "/back - вернуться в главное меню")
        bot.register_next_step_handler(message, areyoushure, IDs, mmss)
    except ValueError:
        abc = bot.send_message(message.chat.id, "Нет такого ID")
        time.sleep(2)
        bot.delete_message(abc.chat.id, abc.message_id)
        start(mmss)


def areyoushure(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == f"я хочу удалить стикер {IDs}":
        print(f"        > deleting accepted!")
        print(f"        > deleted sticker!")
        cursor.execute('DELETE FROM audio WHERE ID = ?', (IDs,))
        conn.commit()
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id, text="Стикер удален (")
        time.sleep(2)
        main_menu(mmss)
    else:
        print(f"        < ABORTED")
        main_menu(mmss)