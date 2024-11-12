import time

from MODULES.BD.init import check_user_last_time, cursor, conn
from MODULES.BOT.init import bot
from MODULES.IMGs.TEXT2IMG import txt2img


def start_generate_txt2_img(message):
    print(">>> GENERATE func.")
    PROMPT = message.text[len('/generate '):].strip()
    args = str(PROMPT).split(" ")
    if len(args) >= 1:
        if PROMPT == "":
            print("    > INCORRECT ARGs")
            fff = bot.send_message(message.chat.id, "Неправильный вызов команды\n"
                                                    "> попробуйте написать так:\n"
                                                    "`/generate кот в облаках`", parse_mode="Markdown")
        else:
            print(f"    > Generation by prompt: {PROMPT}, BY {message.from_user.username}")
            fff = bot.send_message(message.chat.id, "Генерация запущена, подожди чуть-чуть!")

            s_time = time.time()
            Scr = txt2img(PROMPT, message.from_user.username)
            e_time = time.time()
            bot.delete_message(message.chat.id, fff.message_id)
            print(f"      > Generation SUCCESSFULLY : elapsed {round(float(e_time - s_time), 2)}sec")

            if PROMPT == "":
                # bot.send_photo(message.chat.id, open(Scr, 'rb'),
                #                fd"generated by command: \n"
                #                fd">> /generate очень пушистый милый кот в шляпе, 3D мир, Blender, Рендеринг\n\n"
                #                fd"elapsed: ~{round(float(e_time - s_time), 2)}sec")

                pass
            else:
                check_user_last_time(message, added_img=True)
                gen_photo = bot.send_photo(message.chat.id, open(Scr, 'rb'),
                                           f"generated by command: \n>> /generate {PROMPT}\n\n"
                                           f"elapsed: ~{round(float(e_time - s_time), 2)}sec")
                cursor.execute('INSERT INTO genlist (PROMPT, BY, FILE_ID) VALUES (?, ?, ?)',
                               (PROMPT, f"@{message.from_user.username}",
                                gen_photo.photo[-1].file_id))
                conn.commit()
    else:
        print("    > INCORRECT ARGs")
        bot.send_message(message.chat.id, "Неправильный вызов команды, попробуй ещё!")