import requests
from telebot import types

from MODULES.BD.init import cursor, conn
from MODULES.BOT.init import bot


def confirm_f2a(message):
    user = message.chat.id
    idu = (user,)

    cursor.execute(f'SELECT ID FROM admins')
    ADM_USER = cursor.fetchall()

    cursor.execute(f'SELECT ID FROM banlist')
    BaNNED_USER = cursor.fetchall()

    cursor.execute(f'SELECT F2A FROM admins WHERE ID = ?',
                   (message.chat.id,))
    F2A_status = cursor.fetchall()

    bot.delete_message(message.chat.id, message.message_id)

    if idu in ADM_USER and idu not in BaNNED_USER and F2A_status[0][0] == "False":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить номер Номер телефона", request_contact=True)
        keyboard.add(button_geo)
        mmss = bot.send_message(message.chat.id, "Привет, это процедура добавления F2A, сначала отправь номер телефона",
                                reply_markup=keyboard)
        bot.register_next_step_handler(message, handle_contact, mmss)
    else:
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("в главное меню 👌", callback_data="main_menu")
        markup.add(back)
        bot.send_message(message.chat.id, "Вы не админ, или уже добавили F2A!!!", reply_markup=markup)


def handle_contact(message, mmss):
    bot.delete_message(message.chat.id, mmss.message_id)
    if message.contact is not None:
        print(type(message.contact.phone_number))
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить геопозицию", request_location=True)
        keyboard.add(button_geo)
        mmss = bot.send_message(message.chat.id, "Спасибо, теперь последний этап, отправь геопозицию!"
                                                 "(после нажатия кнопки подожди несколько секунд)",
                                reply_markup=keyboard)
        cursor.execute(f'UPDATE admins SET NUMBER_PHONE = ? WHERE ID = ?',
                       (message.contact.phone_number, message.chat.id))
        conn.commit()

        bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, handle_location, mmss)
    else:
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("в главное меню 👌", callback_data="main_menu")
        markup.add(back)
        bot.send_message(message.chat.id, "Ошибка, попробуйте снова", reply_markup=markup)


def handle_location(message, mmss):
    bot.delete_message(message.chat.id, mmss.message_id)
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = get_address(latitude, longitude)
        geo = f"🗺️ {address}"
        mmss = bot.send_message(message.chat.id, "Спасибо, активируем F2A!!!",
                                reply_to_message_id=message.message_id)
        cursor.execute(f'UPDATE admins SET GEO = ?, F2A = ? WHERE ID = ?',
                       (geo, "True", message.chat.id))
        conn.commit()

        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("в главное меню 👌", callback_data="main_menu")
        markup.add(back)

        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=mmss.message_id, text="F2A активирован!!!", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("в главное меню 👌", callback_data="main_menu")
        markup.add(back)
        bot.send_message(message.chat.id, "Ошибка, попробуйте снова", reply_markup=markup)


def get_address(latitude, longitude):
    url = f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'display_name' in data:
            return data['display_name']
        else:
            return "Адрес не найден."
    else:
        return "Ошибка при запросе к API."