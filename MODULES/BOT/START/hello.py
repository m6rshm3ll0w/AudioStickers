import time

from telebot import types

from MODULES.BD.init import check_user_last_time, cursor
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.init import bot


def start(message):
    print(">>> user send a /start command")
    user = message.chat.id
    idu = (user,)
    check_user_last_time(message)
    cursor.execute(f'SELECT ID FROM banlist')
    BaNNED_USER = cursor.fetchall()

    cursor.execute(f'SELECT ID FROM admins')
    ADM_USER = cursor.fetchall()

    cursor.execute(f'SELECT F2A FROM admins WHERE ID = ?',
                   (message.chat.id,))
    F2A_status = cursor.fetchall()

    print(F2A_status)

    if idu in ADM_USER and idu not in BaNNED_USER and F2A_status[0][0] == "False":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        empty = types.KeyboardButton("/skip")
        markup.add(empty)
        sent_message = bot.send_message(message.chat.id,
                                        text=f"@{message.from_user.username} вы админ!\n"
                                             f"но для подтверждения личности вам нужно отправить нам свою геопозицию"
                                             f" и номер телефона... для прохождения проверки введите /F2A либо можете "
                                             f"пропустить этот этап и тогда ваше админство отменяется, "
                                             f"если в течении "
                                             f"2 недель после назначения вы не отправите эти данные, "
                                             f"команда бота @asmembot\n\n"
                                             f"для пропуска нажмите /skip\n"
                                             f"по вопросам пишите 'm1k0.netlify.app/botform' ", reply_markup=markup)
        time.sleep(15)
        main_menu(sent_message)
    else:
        sent_message = bot.send_message(message.chat.id, "Запуск...")
        check_user_last_time(message)

        main_menu(sent_message)