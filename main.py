import uuid
from telebot import *
import sqlite3
from TEXT2IMG import txt2img
import time
import logging
import os
import shutil
from datetime import datetime
import sys

def clear():
    print("clearing --- OK")
    while True:
        if datetime.now().hour == 0 and datetime.now().minute == 00:
            print(f"RESTARTING at {datetime.now()}")
            bot.stop_polling()
            shutil.rmtree('/audio')
            shutil.rmtree('/img')
            os.mkdir('/audio')
            os.mkdir('/img')
            print(f"DONE at {datetime.now()}")
            poooling_bot()


thread = threading.Thread(target=clear)
thread.start()



print(f"\n\nSTARTING BOT PROCESS: ")
start_time = time.time()
print(f" > INITIALISE A BOT ..... ", end="")
try:
    bot = telebot.TeleBot("7426229975:AAH46MNDug2wmHlOfhBlgUmL7SrjxhFX4gM")
    print("DONE")
except Exception as e:
    print("NO\n"
          f"ERROR: {e}")
    exit()

print(f" > CONNECTING TO DB ..... ", end="")
try:
    conn = sqlite3.connect("Dbase.db3", check_same_thread=False)
    print("DONE")
except Exception as e:
    print("NO\n"
          f"ERROR: {e}")
    exit()

print(f" > CREATING DB CURSOR ... ", end="")
try:
    cursor = conn.cursor()
    print("DONE")
except Exception as e:
    print("NO\n"
          f"ERROR: {e}")
    exit()

print(f" > INITIALISE ADMINS .... ", end="")
Audio_Chat = [6615328766, 5184525440]
print("DONE")

end_time = time.time()
# noinspection SpellCheckingInspection
print(f'STARTING BOT PROCESS .... DONE (elapsed: ~{round(float(end_time - start_time), 3)}sec)\n'
      f'--------------------------------------------\n'
      f' > BOT NAME      : @asmembot\n'
      f' > BOT ADMINS    : {Audio_Chat}\n'
      f'--------------------------------------------\n'
      f' > NOW TIME      : {datetime.now()}\n'
      f' > AUTHOR        : @m6rshm3ll0w\n'
      f'--------------------------------------------\n'
      f'!!! bot waiting INLINE REQUEST or COMMAND /start !!!')
time.sleep(2)
print("\n\nStarting TELECLI beta for @asmembot \n", end="")


def ADDD_Audio(voice):
    print(f"    > rendered audio: ID{voice[0]}")
    v = types.InlineQueryResultAudio(
        id=f"{voice[0]}",
        title=f"{voice[1]}",
        audio_url=voice[2])

    return v


def ADDD_PHOTO(photo):
    v = types.InlineQueryResultCachedPhoto(
        id=f"{photo[0]}", photo_file_id=f"{photo[3]}", title=f"{photo[1]}", description=f"{photo[2]}"
    )

    return v


Search_icon = "https://cdn3.iconfinder.com/data/icons/feather-5/24/search-512.png"
PAGE = 1


@bot.inline_handler(func=lambda query: True)
def handle_inline_query(query):
    result = []
    query_text = query.query
    print("ACTIVE INLINE MODE ▼")

    if query_text:

        if query_text.startswith("$"):
            print(">>> user searching genlist:\n")
            query_text = query_text[1:]
            if query_text != "":
                header = types.InlineQueryResultArticle(
                    id='0',
                    title="Поиск по генерациям:",
                    description=f"Промпт: {query_text}",
                    input_message_content=types.InputTextMessageContent(message_text=f"Поиск по генерациям: "
                                                                                     f"{query_text}"),
                    thumbnail_url=Search_icon,
                )
                result.append(header)
            else:
                pass
            cursor.execute(f'SELECT * FROM genlist WHERE PROMPT LIKE ?', (f"%{query_text}%",))
            genlist = cursor.fetchall()
            for photo in genlist:
                result.append(ADDD_PHOTO(photo))

        elif query_text.startswith("@"):
            print(">>> user searching by author:\n"
                  f"    > author: {query_text}")
            header = types.InlineQueryResultArticle(
                id='0',
                title="Поиск по авторам:",
                description=f"стикер, автор которого {query_text}",
                input_message_content=types.InputTextMessageContent(message_text=f"Поиск по авторам: {query_text}"),
                thumbnail_url=Search_icon,
            )
            result.append(header)
            cursor.execute(f'SELECT * FROM audio WHERE DESCRIPTION LIKE ?', (f"%{query_text}%",))
            authors = cursor.fetchall()
            for voice in authors:
                result.append(ADDD_Audio(voice))


        elif query_text.startswith("#"):
            print(">>> user searching by tag:\n"
                  f"    > tag: {query_text}")
            header = types.InlineQueryResultArticle(
                id='0',
                title="Поиск по тегам(если есть):",
                description=f"стикер, у которого есть тег {query_text}",
                input_message_content=types.InputTextMessageContent(message_text=f"Поиск по авторам: {query_text}"),
                thumbnail_url=Search_icon,
            )
            result.append(header)
            cursor.execute(f'SELECT * FROM audio WHERE TAGS LIKE ?', (f"%{query_text}%",))
            authors = cursor.fetchall()
            for voice in authors:
                result.append(ADDD_Audio(voice))

        elif query_text.isdigit():
            print(">>> user searching by page:\n"
                  f"    > page: {query_text}")
            VIEWED_PAGE = int(query_text)
            header = types.InlineQueryResultArticle(
                id='0',
                title="Поиск по страницам",
                description=f"стикеры на странице №{VIEWED_PAGE}",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"Поиск по номеру страницы: №{VIEWED_PAGE}"),
                thumbnail_url=Search_icon,
            )
            result.append(header)
            cursor.execute('SELECT * FROM audio')
            Voices = cursor.fetchall()
            start_index = 49 * (VIEWED_PAGE - 1)
            end_index = 49 * VIEWED_PAGE
            for x, voice in enumerate(Voices[start_index:end_index], start=start_index):
                result.append(ADDD_Audio(voice))

        else:
            print(">>> user searching by name:\n"
                  f"    > name: {query_text}")
            header = types.InlineQueryResultArticle(
                id='0',
                title="Поиск по названию", description=f"фраза '{query_text}' входит в название стикера",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"Поиск по названию: {query_text}"),
                thumbnail_url=Search_icon,
            )
            result.append(header)
            cursor.execute('SELECT * FROM audio WHERE NAME LIKE ?', (f"%{query_text}%",))
            authors = cursor.fetchall()
            for voice in authors:
                result.append(result.append(ADDD_Audio(voice)))

    else:
        print(">>> loading base page")
        header = types.InlineQueryResultArticle(
            id='0',
            title="для справки по поиску",
            description="нажми 'перейти к боту' и в чате нажми \n'как пользоваться', также ты можешь генерировать "
                        "изображения",
            input_message_content=types.InputTextMessageContent(message_text="Для справки по поиску"),
            thumbnail_url=Search_icon,
        )
        result.append(header)
        cursor.execute('SELECT * FROM audio')
        Voices = cursor.fetchall()
        for x, voice in enumerate(Voices[:49]):
            result.append(result.append(ADDD_Audio(voice)))

    bot.answer_inline_query(query.id, result, switch_pm_text="перейти к боту / добавить стикер",
                            switch_pm_parameter="start")


@bot.message_handler(commands=["start"])
def start(message):
    print(">>> user send a /start command")
    sent_message = bot.send_message(message.chat.id, "Запуск...")
    main_menu(sent_message)


def main_menu(message):
    print("    > loading a main_menu")
    markup = types.InlineKeyboardMarkup()
    about = types.InlineKeyboardButton("О создателях / Инфо", callback_data="about")
    mems = types.InlineKeyboardButton("Все войс-стикеры", callback_data="allmems")
    addsticker = types.InlineKeyboardButton("Добавить стикер", callback_data="addsticker")
    howto = types.InlineKeyboardButton("Как пользоваться?", callback_data="howto")
    webUrl = types.WebAppInfo("https://donate.stream/m6rshm3ll0w")
    link_to_app = types.InlineKeyboardButton("💳 Поддержать", web_app=webUrl)
    channel = types.InlineKeyboardButton("канал", "https://t.me/asmemc")
    markup.add(about, link_to_app)
    markup.add(mems, addsticker)
    markup.add(howto, channel)
    if message.chat.id in Audio_Chat:
        adm = types.InlineKeyboardButton("👇👇Возможности админов👇👇", callback_data="0")
        edit_msg = types.InlineKeyboardButton("редактировать стикер", callback_data="edit_s")
        del_msg = types.InlineKeyboardButton("удалить стикер", callback_data="del_s")
        markup.add(adm)
        markup.add(edit_msg, del_msg)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=">>>> админ-панель\n"
                                   "@asmemc - канал с новостями\n\n"
                                   "👋 Привет, это бот для того, чтобы "
                                   "все смешные голосовые"
                                   "сообщения и аудио-мемы "
                                   "были в сборе и ты мог их быстро отправлять своим друзьям "
                                   "или в комментариях в каналах \n\n"
                                   "!!! Если в описании видите пометку R18 - "
                                   "это обозначает, что у данного аудио стикера рейтинг 18+, будьте внимательны !!!\n"
                                   "Все стикеры модерируются!!!\n\n"
                                   "1.0 - генерация картинок\n"
                                   " > Напиши '/generate (твой промпт)' и подожди ~20сек\n\n"
                                   "Ниже есть кнопки, выбери что хочешь сделать 👇",
                              reply_markup=markup)

    elif message.chat.id != Audio_Chat:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                              text=">>>> админ-панель\n"
                                   "@asmemc - канал с новостями\n\n"
                                   "👋 Привет, это бот для того, чтобы "
                                   "все смешные голосовые"
                                   "сообщения и аудио-мемы "
                                   "были в сборе и ты мог их быстро отправлять своим друзьям "
                                   "или в комментариях в каналах \n\n"
                                   "!!! Если в описании видите пометку R18 - "
                                   "это обозначает, что у данного аудио стикера рейтинг 18+, будьте внимательны !!!\n"
                                   "Все стикеры модерируются!!!\n\n"
                                   "1.0 - генерация картинок\n"
                                   " > Напиши '/generate (твой промпт)' и подожди ~20сек\n\n"
                                   "Ниже есть кнопки, выбери что хочешь сделать 👇",
                              reply_markup=markup)


def all_s(message):
    print("    >> loading a viewer")
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("В главное меню 😉", callback_data="main_menu")
    markup.add(back)
    PAGES = 1
    cursor.execute('SELECT * FROM audio')
    Voices = cursor.fetchall()
    result = "Все аудио стикеры:\n"

    if 1 <= len(Voices) <= 49:
        PAGES = 1
    elif len(Voices) % 49 != 0:
        PAGES = len(Voices) // 2 + 1
    elif len(Voices) % 49 == 0:
        PAGES = len(Voices) // 2
    elif len(Voices) == 0:
        PAGES = 1
        result = result + (" пока тут пусто\n"
                           " добавь свой аудио-стикер!")

    if PAGE == 1 and PAGES != 1:
        left = types.InlineKeyboardButton("<-", callback_data="0")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="page+1")
        markup.add(left, list_p, right)
    elif PAGE == PAGES and PAGES != 1:
        left = types.InlineKeyboardButton("<-", callback_data="page-1")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="0")
        markup.add(left, list_p, right)
    elif 1 < PAGE > PAGES:
        left = types.InlineKeyboardButton("<-", callback_data="page-1")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="page+1")
        markup.add(left, list_p, right)
    else:
        left = types.InlineKeyboardButton("<-", callback_data="0")
        list_p = types.InlineKeyboardButton(f"{PAGE}/{PAGES}", callback_data="0")
        right = types.InlineKeyboardButton("->", callback_data="0")
        markup.add(left, list_p, right)

    start_index = 49 * (PAGE - 1)
    end_index = 49 * PAGE
    for x, voice in enumerate(Voices[start_index:end_index], start=start_index):
        f = (f"ID {voice[0]}\n"
             f"NAME    : {voice[1]}\n"
             f"> DESC. : {voice[3]}\n\n")
        result = result + f
    bot.edit_message_text(text=result, chat_id=message.chat.id, message_id=message.id, reply_markup=markup)


# noinspection SpellCheckingInspection
@bot.callback_query_handler(func=lambda callback: True)
def handler(callback):
    print(">>> callback")
    global PAGE
    if callback.data == "about":
        print("    > page about")
        cursor.execute(f'SELECT * FROM audio')
        Stickers = cursor.fetchall()
        n_of_s = len(Stickers)
        AUTHORS = (f"....... code .......  v1.0 ß\n"
                   "... @m6rshm3ll0w ...  @asmembot\n"
                   f"....................  ▼ stickers ▼\n"
                   f"....... audio ......  {n_of_s}\n"
                   "...... @VaLm1n .....\n"
                   ".... @YltraPablo ...")

        bot.answer_callback_query(callback_query_id=callback.id, text=AUTHORS,
                                  show_alert=True)

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
                              "Для упрощения использования, тут есть поиск: \n"
                              "-> по авторам - @\n"
                              "-> по названию\n"
                              "-> по страницам\n"
                              "-> по тегам - #\n"
                              "-> ранее сгенерированные картинки - $\n"
                              "!!! Если в описании видите пометку R18 - "
                              "это обозначает, что у данного аудиостикера рейтинг 18+, будьте внимательны !!!\n"
                              "Все стикеры модерируются!!!\n\n"
                              "\n"
                              "вот и все, так просто\n"
                              "\n"
                              "П.С содержание страниц и номера стикеров можешь посмотреть через пункт \n"
                              "'все войс-стикеры' 🤗",
                              callback.message.chat.id,
                              callback.message.id, reply_markup=markup)

    elif callback.data == "allmems":
        print("    > viewer page")
        PAGE = 1
        all_s(callback.message)

    elif callback.data == "page+1":
        PAGE += 1
        print(f"    > viewer page {PAGE}")
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
        PAGE -= 1
        print(f"    > viewer page {PAGE}")
        all_s(callback.message)

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
                   "2.Добавте '(R18)', если рейтинг аудио 18+\n"
                   "3.За 2 нарушения правил вы получаете предупреждение, "
                   "а за 3 - вы не можете добавлять стикеры")
        bot.answer_callback_query(callback_query_id=callback.id, text=LICENSE,
                                  show_alert=True)


def D_S(message, mmss):
    print(f"      > del sticker {message.text}")
    bot.delete_message(message.chat.id, message.message_id)
    try:
        IDs = int(message.text)
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id,
                                     text="Ты точно хочешь удалить стикер из базы данных, если да то напиши \n"
                                          " >>> я хочу удалить стикер (ID стикера)\n"
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
        cursor.execute(f'DELETE from audio WHERE ID = ?',
                       f"{IDs}")
        conn.commit()
        mmss = bot.edit_message_text(chat_id=mmss.chat.id, message_id=mmss.message_id, text="Стикер удален (")
        time.sleep(2)
        main_menu(mmss)
    else:
        print(f"        < ABORTED")
        main_menu(mmss)


def E_S_P(message, mmss):
    try:
        print(f"      > edit sticker {message.text}")
        IDs = int(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        e_t = types.KeyboardButton("название")
        e_tags = types.KeyboardButton("теги")
        e_description = types.KeyboardButton("описание")
        e_id = types.KeyboardButton("id")
        mm = types.KeyboardButton("назад")
        markup.add(e_t, e_tags)
        markup.add(e_description, e_id)
        markup.add(mm)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Выбери что изменить ", reply_markup=markup)
        bot.register_next_step_handler(message, E_S_P2, IDs, mmss)
    except ValueError:
        print(f"      > INVALID S_ID")
        mmss = bot.send_message(message.chat.id, "такого id нет....")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        main_menu(message)


def E_S_P2(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(mmss.chat.id, mmss.message_id)
    if str(message.text) == "название":
        print(f"        > NAME")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ На что хочешь изменить название?\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, EN, IDs, mmss)
    if str(message.text) == "теги":
        print(f"        > TAGS")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > tags {str(FILE_id[0][4])}\n"
                                                      f"‖ Введи желаемые теги.\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, ET, IDs, mmss)
    if str(message.text) == "id":
        print(f"        > ID")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > ID {str(FILE_id[0][0])}\n"
                                                      f"‖ Введи желаемый id.\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, EID, IDs, mmss)
    if str(message.text) == "описание":
        print(f"        > DESCRIPTION")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()
        mmss = bot.send_message(message.chat.id, text=f"‖ name = {FILE_id[0][1]}\n"
                                                      f"‖ > desc. = {FILE_id[0][3]}\n"
                                                      f"‖ > tags {str(FILE_id[0][4])}\n"
                                                      f"‖ Введи желаемое описание (откуда этот звук).\n"
                                                      f"напиши /back , чтобы выйти в главное меню")
        bot.register_next_step_handler(message, ED, IDs, mmss)
    if str(message.text) == "назад":
        print(f"        < EXITED")
        start(message)


def EN(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW NAME: {message.text}")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()

        try:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)
        except AttributeError:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)

        BY = str(FILE_id[0][3]).split(" ● ")[0]

        FID = str(uuid.uuid4())
        SCR = f'audio/{BY}'
        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        with open(f"{SCR}/{FID}.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        fid = bot.send_audio(message.chat.id,
                             audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                             title=f"{message.text}",
                             performer=f"{FILE_id[0][3]}")
        cursor.execute(f'UPDATE audio SET FILE_ID = ?, NAME = ? WHERE ID = ?',
                       (fid.voice.file_id, message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(3)
        bot.delete_message(fid.chat.id, fid.message_id)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def ET(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW TAGS: {message.text}")
        cursor.execute(f'UPDATE audio SET TAGS = ? WHERE ID = ?',
                       (message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def EID(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW ID: {message.text}")
        cursor.execute(f'UPDATE audio SET ID = ? WHERE ID = ?',
                       (message.text, IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


def ED(message, IDs, mmss):
    bot.delete_message(message.chat.id, message.message_id)
    if message.text == '/back':
        print(f"          < ABORTED")
        main_menu(mmss)
    else:
        print(f"          > NEW DESCR. : {message.text}")
        cursor.execute(f'SELECT * FROM audio WHERE ID = ?', f"{IDs}")
        FILE_id = cursor.fetchall()

        try:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)
        except AttributeError:
            file_info = bot.get_file(FILE_id[0][2])
            downloaded_file = bot.download_file(file_info.file_path)

        BY = str(FILE_id[0][3]).split(" ● ")[0]

        FID = str(uuid.uuid4())
        SCR = f'audio/{BY}'
        if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
            path = os.path.join(os.getcwd(), SCR)
            os.mkdir(path)

        with open(f"{SCR}/{FID}.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        DESCRIPTION = f"{BY} ● {message.text}"
        if len(DESCRIPTION) < 43:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                                 title=f"{FILE_id[0][1]}",
                                 performer=f"{DESCRIPTION[:len(DESCRIPTION) - 43]}\n{DESCRIPTION[43:]}")
        else:
            fid = bot.send_audio(message.chat.id,
                                 audio=open(f"{SCR}/{FID}.ogg", 'rb'),
                                 title=f"{FILE_id[0][1]}",
                                 performer=f"{DESCRIPTION}")

        cursor.execute(f'UPDATE audio SET FILE_ID = ?, DESCRIPTION = ? WHERE ID = ?',
                       (fid.voice.file_id, f"{DESCRIPTION}", IDs))
        conn.commit()
        bot.delete_message(mmss.chat.id, mmss.message_id)
        mmss = bot.send_message(message.chat.id, "Аудио-стикер обновлен!!!")
        time.sleep(2)
        bot.delete_message(mmss.chat.id, mmss.message_id)
        start(message)


# noinspection SpellCheckingInspection
@bot.message_handler(content_types=["audio", "voice"])
def add_sticker(message):
    print(f">>> ADDING A STICKER by @{message.from_user.username}")
    audio = message
    markup = types.InlineKeyboardMarkup()
    licensea = types.InlineKeyboardButton("УСЛОВИЯ", callback_data="license")
    markup.add(licensea)
    bot.send_message(message.chat.id, "Создавая стикер вы принимаете условия\n\n"
                                      "Придумайте название для стикера....\n"
                                      "напишите /back если не хотите создавать стикер", reply_markup=markup)
    bot.register_next_step_handler(message, sticker_name, audio)


def sticker_name(message, audio):
    if message.text == "/back":
        print("<<< ABORTED")
        start(message)
    else:
        name = message.text
        print(f"    > NAME: {name}")

        bot.send_message(message.chat.id,
                         "ОК, теперь выбери эмодзи для стикера...\n"
                         "если эмодзи нет просто напишите \n/empty")
        bot.register_next_step_handler(message, sticker_emoji, audio, name)


def sticker_emoji(message, audio, name):
    if message.text == "/empty":
        print(f"      > emoji SKIPPED >")
        NAME = name
        print(f"      > FULL NAME: {NAME}")
    else:
        EMOJI = message.text
        NAME = EMOJI + " " + name
        print(f"      > EMOJI: {EMOJI}")
        print(f"      > FULL NAME: {NAME}")
    bot.send_message(message.chat.id, "ОК, теперь напиши теги в формате:\n"
                                      "#tag1 #tag2 #tag3...\n"
                                      "если тегов нет просто напишите \n/empty")
    bot.register_next_step_handler(message, sticker_description, audio, NAME)


def sticker_description(message, audio, NAME):
    if message.text == "/empty":
        TAGS = "#пусто"
        print(f"        > tag SKIPPED >")
    else:
        TAGS = message.text
        print(f"        > TAGS: {TAGS}")

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    r18 = types.KeyboardButton("(R18)")
    markup.add(r18)
    bot.send_message(message.chat.id, "ОК, теперь напиши описание(откуда этот трек или его настоящий автор):\n"
                                      "!!! если стикер не предназначен для совершеннолетней аудитории допишите (R18)\n"
                                      "если описания нет просто напишите \n/empty", reply_markup=markup)
    bot.register_next_step_handler(message, sticker_to_base, audio, NAME, TAGS)


def sticker_to_base(message, audio, NAME, TAGS):
    BY = f"{message.from_user.username}"

    if message.text == "/empty":
        DESCRIPTION = f"@{BY} ● "
        print(f"          > descr. SKIPPED >")
    else:
        DESCRIPTION = f"@{BY} ● {message.text}"
        print(f"          > DESCR. : {DESCRIPTION}")

    try:
        file_info = bot.get_file(audio.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except AttributeError:
        file_info = bot.get_file(audio.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

    FID = str(uuid.uuid4())
    SCR = f'audio/@{BY}'

    if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
        path = os.path.join(os.getcwd(), SCR)
        os.mkdir(path)

    SCR = f"{SCR}/{FID}.ogg"

    with open(SCR, 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()

    if len(DESCRIPTION) < 43:
        fid = bot.send_audio(message.chat.id,
                             audio=open(SCR, 'rb'),
                             title=f"{NAME}",
                             performer=f"{DESCRIPTION[:len(DESCRIPTION) - 43]}\n{DESCRIPTION[43:]}")
    else:
        fid = bot.send_audio(message.chat.id,
                             audio=open(SCR, 'rb'),
                             title=f"{NAME}",
                             performer=f"{DESCRIPTION}")

    cursor.execute('INSERT INTO audio (NAME, FILE_ID, DESCRIPTION, TAGS) VALUES (?, ?, ?, ?)',
                   (NAME, fid.voice.file_id, DESCRIPTION, TAGS))
    conn.commit()
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("в главное меню 👌", callback_data="main_menu")
    markup.add(back)
    bot.send_message(message.chat.id, "Отлично, стикер добавлен!!! "
                                      f"Data:\n"
                                      f"   -name  :{NAME}\n"
                                      f"   -by    :{BY}\n"
                                      f"   -desc. :{DESCRIPTION}", reply_markup=markup)

    print(f"            > STICKER ADDED SUCCESSFUL")


@bot.message_handler(commands=["generate"])
def start_generate_txt2_img(message):
    print(">>> GENERATE func.")
    text = message.text[len('/generate '):].strip()
    args = str(text).split(" ")
    if len(args) >= 1:
        if text == "":
            print("    > INCORRECT ARGs")
            fff = bot.send_message(message.chat.id, "Неправильный вызов команды\n"
                                                    "> запуск со стандартным промптом")
            text = "очень пушистый милый кот в шляпе, 3D мир, Blender, Рендеринг"
        else:
            print(f"    > Generation by prompt {text}, BY {message.from_user.username}")
            fff = bot.send_message(message.chat.id, "Генерация запущена, подожди чуть-чуть!")

        s_time = time.time()
        Scr = txt2img(text, message.from_user.username)
        e_time = time.time()
        bot.delete_message(message.chat.id, fff.message_id)
        print(f"      > Generation SUCCESSFULLY : elapsed {round(float(e_time - s_time), 2)}sec")
        gen_photo = bot.send_photo(message.chat.id, open(Scr, 'rb'), f"generated by command: \n>> /generate {text}\n\n"
                                                                     f"elapsed: ~{round(float(e_time - s_time), 2)}sec")
        cursor.execute('INSERT INTO genlist (PROMPT, BY, FILE_ID) VALUES (?, ?, ?)',
                       (text, f"@{message.from_user.username}", gen_photo.photo[-1].file_id))
        conn.commit()
    else:
        print("    > INCORRECT ARGs")
        bot.send_message(message.chat.id, "Неправильный вызов команды, попробуй ещё!")


# noinspection SpellCheckingInspection
def poooling_bot():
    while True:
        try:
            print("\nHELLO, THIS IS TELECLI - debug CLI interface for @asmembot\n", end="")
            logging.info(" BOT RUNNING..... DONE")
            bot.polling(none_stop=True, interval=2)
            sys.exit()
        except Exception as Except_:

            print("\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))

            print("RESTARTING...", end="")
            bot.stop_polling()

            time.sleep(10)

            print("DONE\n\n>>>")


poooling_bot()