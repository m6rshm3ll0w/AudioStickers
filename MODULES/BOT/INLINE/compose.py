from dotenv import dotenv_values
from telebot import types

from MODULES.BD.init import cursor
from MODULES.BOT.INLINE.inline_content import ADDD_Chatgpt, ADDD_PHOTO, ADDD_Audio
from MODULES.BOT.init import bot
from MODULES.OTHER.global_init import ChatGPT, Search_icon, Chatgpt_ICON


def inline_viewer(query):
    result = []
    query_text = query.query
    print("ACTIVE INLINE MODE ▼")

    if query_text:
        if query_text.startswith("&"):
            print(f">>> user usig chatgpt: {query_text}\n")
            query_text = query_text[1:]
            if query_text.endswith("#") and ChatGPT:
                query_text = query_text[:len(query_text) - 1]
                print(query_text)
                header = types.InlineQueryResultArticle(
                    id='-1',
                    title="Запрос к ChatGpt:",
                    description=f"Промпт: {query_text}",
                    input_message_content=types.InputTextMessageContent(message_text=f"Запрос к ChatGpt: "
                                                                                     f"{query_text}"),
                    thumbnail_url=Search_icon,
                )
                result.append(header)
                result.append(ADDD_Chatgpt(query_text))
            else:
                header = types.InlineQueryResultArticle(
                    id='-1',
                    title="ChatGPT",
                    description="В конце промпта напиши # для запроса",
                    input_message_content=types.InputTextMessageContent(message_text=f"Запрос к ChatGpt: "
                                                                                     f"{query_text}"),
                    thumbnail_url=Chatgpt_ICON,
                )
                result.append(header)

        elif query_text.startswith("$"):
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
            for photo in genlist[:49]:
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
            Voices = cursor.fetchall()

            for voice in Voices[:49]:
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
            Voices = cursor.fetchall()

            for voice in Voices[:49]:
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
            for voice in enumerate(Voices[start_index:end_index], start=start_index):
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
            Voices = cursor.fetchall()

            for voice in Voices[:49]:
                result.append(ADDD_Audio(voice))

    else:
        print(">>> loading base page")
        header = types.InlineQueryResultArticle(
            id='0',
            title="Стикеры",
            description="для справки по поиску нажми 'перейти к боту' и в чате нажми \n"
                        "'как пользоваться'",
            input_message_content=types.InputTextMessageContent(message_text="-"),
            thumbnail_url=Search_icon,
        )
        result.append(header)
        cursor.execute('SELECT * FROM audio')
        Voices = cursor.fetchall()
        # random.shuffle(Voices)
        for voice in Voices[:49]:
            result.append(ADDD_Audio(voice))

    bot.answer_inline_query(query.id, result, switch_pm_text="перейти к боту / добавить стикер",
                            switch_pm_parameter="start")