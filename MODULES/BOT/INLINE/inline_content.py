from dotenv import dotenv_values
from telebot import types

from MODULES.GROQ.init import client
from MODULES.OTHER.global_init import Chatgpt_ICON


def ADDD_Audio(voice):
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


def ADDD_Chatgpt(text):
    print(f"    > render ask:{text}")
    print(text)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Ты вежливый помощник, который отвечает достаточно кратко и понятно на Русском языке"
            },
            {
                "role": "user",
                "content": f"{text}",
            }
        ],
        model="llama3-8b-8192",
        max_tokens=3000,

    )

    ask = chat_completion.choices[0].message.content

    if len(ask) > 43:
        v = types.InlineQueryResultArticle(id="0", thumbnail_url=Chatgpt_ICON, title="Chatgpt",
                                           description=f"{ask[:len(ask) - 43]}\n{ask[43:]}",
                                           input_message_content=types.InputTextMessageContent(
                                               message_text=f"---- ChatGpt ----\n"
                                                            f"{ask}", parse_mode="Markdown"))
    else:
        v = types.InlineQueryResultArticle(id="0", thumbnail_url=Chatgpt_ICON, title="Chatgpt", description=f"{ask}",
                                           input_message_content=types.InputTextMessageContent(
                                               message_text=f"---- ChatGpt ----\n"
                                                            f"{ask}", parse_mode="Markdown"))

    return v
