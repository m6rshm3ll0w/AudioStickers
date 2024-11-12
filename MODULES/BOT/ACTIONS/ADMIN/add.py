import time
from datetime import datetime

from MODULES.BD.init import cursor, conn
from MODULES.BOT.START.hello import start
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def ADM_ID(message, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        usernamee = message.text
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                     text=f"ОК, теперь введи id {usernamee}\n"
                                          f"или /back для отмены")
        bot.register_next_step_handler(message, ADM_ID2, mmss, usernamee)


def ADM_ID2(message, mmss, usernamee):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:

        print(f"      > add admin {message.text}")
        try:
            IDs = int(message.text)
            mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                         text="Ты точно хочешь добавить админа, если да то напиши \n"
                                              f" >>> я хочу сделать админом {IDs}\n"
                                              "/back - вернуться в главное меню")
            bot.register_next_step_handler(message, ADM_ID_2, IDs, mmss, usernamee)
        except ValueError:
            abc = bot.send_message(message.chat.id, "Нет такого ID")
            time.sleep(2)
            bot.delete_message(abc.chat.id, abc.message_id)
            start(mmss)


def ADM_ID_2(message, IDs, mmss, usernamee):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == f"я хочу сделать админом {IDs}":
        print(f"        > adding acepted")
        cursor.execute("INSERT INTO admins (ID, USERNAME, DATE, F2A) VALUES (?, ?, ?, ?)",
                       (IDs, usernamee, str(datetime.now()).split(' ')[0], "False"))
        conn.commit()
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                     text=f"{usernamee} - админ!\n")
        bot.send_message(IDs, f"{usernamee} вы админ!\n"
                              f"но для подтверждения личности вам нужно отправить нам свою геопозицию"
                              f" и номер телефона... для прохождения проверки введите /F2A либо можете "
                              f"пропустить этот этап и тогда ваше админство отменяется, если в течении "
                              f"2 недель после назначения вы не отправите эти данные, "
                              f"команда бота @asmembot\n\n"
                              f"по вопросам пишите 'm1k0.netlify.app/botform' ")
        time.sleep(2)
        main_menu(mmss)
    else:
        print(f"        < ABORTED")
        main_menu(mmss)
