from dotenv import dotenv_values
from telebot import types

from MODULES.BD.init import cursor
from MODULES.BOT.init import bot
from MODULES.OTHER.global_init import ADMINS

loc_s = dotenv_values("DATA/.env")
VERSION = loc_s["version"]


def main_menu(message, ADMIN_PANEL=True):
    print("    > loading a main_menu")
    main_text = str("@asmemc - канал с новостями "
                    "(подпишитесь пж)\n"
                    "\n"
                    f"**V{VERSION}**\n"
                    "\n"
                    "👋 Привет, это бот для того, чтобы "
                    "все смешные голосовые"
                    "сообщения и аудио-мемы "
                    "были в сборе и ты мог их быстро отправлять своим друзьям "
                    "или в комментариях в каналах \n"
                    "\n"
                    "\n"
                    "**ChangeLog**\n"
                    "1.0 β - генерация картинок и возрастной рейтинг\n"
                    "2.0 - CHAT GPT и статистика пользователей"
                    # "1.1 - ChatGpt и просмотр-отправка ранее генерированных картинок в Inline-режиме\n"
                    "\n"
                    "подробнее о боте во вкладке **'Как пользоваться?'**\n"
                    "Ниже есть кнопки, выбери что хочешь сделать 👇")
    markup = types.InlineKeyboardMarkup()
    about = types.InlineKeyboardButton("О создателях", callback_data="about")
    botform = types.InlineKeyboardButton("Сообщить о баге / предложить идею",
                                         url="https://m1k0.netlify.app/botform/")
    mems = types.InlineKeyboardButton("Все войс-стикеры", callback_data="allmems")
    addsticker = types.InlineKeyboardButton("Добавить стикер", callback_data="addsticker")
    howto = types.InlineKeyboardButton("Как пользоваться?", callback_data="howto")
    webUrl = types.WebAppInfo("https://donate.stream/m6rshm3ll0w")
    link_to_app = types.InlineKeyboardButton("💳 Поддержать", web_app=webUrl)
    channel = types.InlineKeyboardButton("канал", "https://t.me/asmemc")
    markup.add(about, link_to_app)
    markup.add(mems, addsticker)
    markup.add(howto, channel)
    markup.add(botform)

    user = message.chat.id
    idu = (user,)

    cursor.execute(f'SELECT ID FROM banlist')
    BaNNED_USER = cursor.fetchall()

    cursor.execute(f'SELECT ID FROM admins')
    ADM_USER = cursor.fetchall()

    cursor.execute(f'SELECT F2A FROM admins WHERE ID = ?',
                   (message.chat.id,))
    F2A_status = cursor.fetchall()

    if idu in ADM_USER and idu not in BaNNED_USER and F2A_status[0][0] == "True":

        if ADMIN_PANEL:
            adm = types.InlineKeyboardButton("👇👇Возможности админов👇👇", callback_data="admin_panel_dis")
            markup.add(adm)
            edit_msg = types.InlineKeyboardButton("редактировать стикер", callback_data="edit_s")
            del_msg = types.InlineKeyboardButton("удалить стикер", callback_data="del_s")
            ban = types.InlineKeyboardButton("Выдать бан", callback_data="banuser")
            unban = types.InlineKeyboardButton("Убрать бан", callback_data="deladm")
            banl = types.InlineKeyboardButton("Банлист", callback_data="banlist")
            adml = types.InlineKeyboardButton("Админы", callback_data="admlist")
            usrl = types.InlineKeyboardButton("Users", callback_data="userlist")

            markup.add(edit_msg, del_msg)
            markup.add(ban, unban)
            if message.chat.id in ADMINS:
                deladm = types.InlineKeyboardButton("Убрать админку", callback_data="deladm")
                addadm = types.InlineKeyboardButton("Выдать админку", callback_data="addadm")
                backup_db = types.InlineKeyboardButton("Бекап базы данных", callback_data="backupbd")
                markup.add(deladm, addadm)
                markup.add(backup_db)

            markup.add(banl, adml, usrl)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                  text=f">>>> админ-панель\n{main_text}",
                                  reply_markup=markup, parse_mode="Markdown")
        else:
            adm = types.InlineKeyboardButton("👇👇Возможности админов👇👇", callback_data="admin_panel")
            markup.add(adm)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                  text=main_text,
                                  reply_markup=markup, parse_mode="Markdown")

    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=main_text,
                              reply_markup=markup, parse_mode="Markdown")