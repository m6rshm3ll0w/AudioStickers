from telebot import types

from MODULES.BD.init import cursor, PREP_BACKUP
from MODULES.BOT.ACTIONS.ADMIN.add import ADM_ID
from MODULES.BOT.ACTIONS.ADMIN.remove import DEL_ADM_U_ID
from MODULES.BOT.ACTIONS.BAN.add import B_U_ID
from MODULES.BOT.ACTIONS.BAN.remove import UB_U_ID
from MODULES.BOT.START.main_menu import main_menu
from MODULES.BOT.STICKERS.EDIT.delete import D_S
from MODULES.BOT.STICKERS.EDIT.edit_data import E_S_P
from MODULES.BOT.VIEWERS.admins import ADM_LIST
from MODULES.BOT.VIEWERS.banned_users import Ban_LIST
from MODULES.BOT.VIEWERS.stickers import all_s, set_page
from MODULES.BOT.VIEWERS.users import USR_LIST
from MODULES.BOT.init import bot
from MODULES.OTHER.global_init import VERSION, code_by, audio_by


def callback_handler_main(callback):
    print(">>> callback")
    if callback.data == "about":
        print("    > page about")
        cursor.execute(f'SELECT * FROM audio')
        Stickers = cursor.fetchall()
        n_of_s = len(Stickers)

        AUTHORS = (f"code {VERSION}\n"
                   f"> {"\n".join(code_by.split("\\n"))}\n"
                   f"_____________________\n"
                   f"audio : {n_of_s}\n"
                   f"> {"\n> ".join(audio_by.split("\\n"))}")
        try:
            bot.answer_callback_query(callback_query_id=callback.id, text=AUTHORS,
                                      show_alert=True)
        except Exception:
            print("ERROR in handler.py : line 35")

    elif callback.data == "main_menu":
        print("    > returning to main_menu")
        main_menu(callback.message)

    elif callback.data == "howto":
        print("    > learn page")
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
        markup.add(back)
        bot.edit_message_text("Использование нашего бота проще чем тебе кажется, "
                              "просто в чате с другом или комментарии напиши @asmembot и выбери войс-стикер, "
                              "если ни один не понравился, можешь добавить свой через этого бота...\n"
                              "Для упрощения использования, тут есть поиск \n"
                              "\n"
                              "**Inline режим** \n"
                              "-> по авторам - @\n"
                              "-> по названию\n"
                              "-> по страницам\n"
                              "-> по тегам - #\n"
                              "-> ранее сгенерированные картинки - $\n"
                              "-> вызов Chat GPT - '&(запрос)#'\n"
                              "\n"
                              "**БОТ**\n"
                              "-> Напиши ```bash /generate (твой промпт)``` и подожди ~20сек\n"
                              "\n"
                              "**ВАЖНОЕ**\n"
                              "Если в описании видите пометку R18 - "
                              "это обозначает, что у данного аудиостикера рейтинг 18+, будьте внимательны !!!\n"
                              "Все стикеры модерируются\n"
                              "\n"
                              "**ПРАВИЛА**\n"
                              "УСЛОВИЯ добавления стикера:\n"
                              "1.Убедитесь, что такого стикера нет\n"
                              "2.Добавьте '(R18)', если рейтинг аудио 18+\n"
                              "3.За 2 нарушения правил вы получаете предупреждение, "
                              "а за 3 - вы не можете добавлять стикеры\n"
                              "\n"
                              "эта страница будет дополняться\n"
                              "вот и все, так просто\n"
                              "\n"
                              "П.С содержание страниц и номера стикеров можешь посмотреть через пункт \n"
                              "'все войс-стикеры' 🤗", parse_mode="Markdown", chat_id=callback.message.chat.id,
                              message_id=callback.message.id, reply_markup=markup)


    elif callback.data == "admin_panel":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        mmss = bot.send_message(chat_id=callback.message.chat.id, text="активация админ-панели...")
        main_menu(mmss, ADMIN_PANEL=True)

    elif callback.data == "admin_panel_dis":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        mmss = bot.send_message(chat_id=callback.message.chat.id, text="деактивация админ-панели...")
        main_menu(mmss, ADMIN_PANEL=False)


    elif callback.data == "allmems":
        print("    > viewer page")
        set_page(1)
        all_s(callback.message)

    elif callback.data == "page+1":
        set_page(1, plus=True)
        all_s(callback.message)

    elif callback.data == "edit_s":
        print("    > editing")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи id стикера для изменения")
        bot.register_next_step_handler(callback.message, E_S_P, mmss)

    elif callback.data == "del_s":
        print("    > deleting")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи id стикера для удаления")
        bot.register_next_step_handler(callback.message, D_S, mmss)

    elif callback.data == "page-1":
        set_page(1, minus=True)
        all_s(callback.message)

    elif callback.data == "banuser":
        print("    > banuser")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи ID человека для добавления в банлист или /back ... ")
        bot.register_next_step_handler(callback.message, B_U_ID, mmss)

    elif callback.data == "unbanuser":
        print("    > unbanuser")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи ID человека для удаления из банлиста или /back ... ")
        bot.register_next_step_handler(callback.message, UB_U_ID, mmss)

    elif callback.data == "admlist":
        print("    > admlist")
        ADM_LIST(callback.message)

    elif callback.data == "userlist":
        print("    > usrlist")
        USR_LIST(callback.message)

    elif callback.data == "backupbd":
        PREP_BACKUP(callback.message)

    elif callback.data == "addadm":
        print("    > add adm")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи имя пользователя (начинается с @, образец: @gsa)"
                                          " для добавления в админы или /back ... ")
        bot.register_next_step_handler(callback.message, ADM_ID, mmss)

    elif callback.data == "deladm":
        print("    > del adm")
        mmss = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                     text="введи ID человека (можно посмотреть в 'админы')"
                                          " для удаления из админов или /back ... ")
        bot.register_next_step_handler(callback.message, DEL_ADM_U_ID, mmss)

    elif callback.data == "banlist":
        print("    > banlist")
        Ban_LIST(callback.message)

    elif callback.data == "del_msg":
        print("    > delmsg")
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == "addsticker":
        print(f"    > adding a sticker(help)")
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("В главное меню 😑", callback_data="main_menu")
        markup.add(back)
        bot.edit_message_text("для добавления своего стикера тебе всего лишь надо отправить мне файл формата "
                              ".mp3 (макс 30 секунд) и следовать инструкциям бота, предупреждение, "
                              "пожалуйста не загружай слишком много однотипных и повторяющихся стикеров,"
                              " иначе админы тебя забанят )))",
                              callback.message.chat.id,
                              callback.message.id, reply_markup=markup)

    elif callback.data == "license":
        LICENSE = ("УСЛОВИЯ добавления стикера:\n"
                   "1.Убедитесь, что такого стикера нет\n"
                   "2.Добавьте '(R18)', если рейтинг аудио 18+\n"
                   "3.За 2 нарушения правил вы получаете предупреждение, "
                   "а за 3 - вы не можете добавлять стикеры")
        bot.answer_callback_query(callback_query_id=callback.id, text=LICENSE,
                                  show_alert=True)
