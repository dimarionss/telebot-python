import config
import telebot
from telebot import types  # кнопки
from string import Template

bot = telebot.TeleBot(config.token)

user_dict = {}
Usluga = ''


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'instagram',
                'dateZapis', 'applyParam', 'Usluga']

        for key in keys:
            self.key = None


# если /help, /start


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Курсы')
    itembtn2 = types.KeyboardButton('Услуги')
    itembtn3 = types.KeyboardButton('Обо мне')

    markup_main.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", выберите действие ⬇", reply_markup=markup_main)


def send_welcome2(message):
    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Курсы')
    itembtn2 = types.KeyboardButton('Услуги')
    itembtn3 = types.KeyboardButton('Обо мне')
    markup_main.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Выберите действие ⬇",
                     reply_markup=markup_main)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Обо мне':
        bot.send_message(message.chat.id, "Мы надежная компания"
                         + " company. 10 лет на рынке.")
    elif message.text == 'Услуги':
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('🌟 Свадебная прическа 🌟')
        itembtn2 = types.KeyboardButton('🌟 Выпускная прическа 🌟')
        itembtn3 = types.KeyboardButton('🌟 Вечерняя прическа 🌟')
        itembtn4 = types.KeyboardButton('🌟 Плетение 🌟')
        itembtn5 = types.KeyboardButton('🌟 Афрокудри 🌟')
        itembtn6 = types.KeyboardButton('🌟 Стрижки 🌟')
        itembtn7 = types.KeyboardButton('🌟 Полировка 🌟')
        markup.add(itembtn1, itembtn2)
        markup.add(itembtn3, itembtn4)
        markup.add(itembtn5, itembtn6)
        markup.add(itembtn7)
        msg = bot.send_message(
            message.chat.id, 'Выберите тип услуги:', reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, process_usluga_step)
    elif message.text == 'Курсы':
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton(
            '🌟 Базовый экспресс-курс по причёскам 🌟')
        itembtn2 = types.KeyboardButton('🌟 Свадебные прически 🌟')
        itembtn3 = types.KeyboardButton('🌟 Прически для себя 🌟')
        markup.add(itembtn1)
        markup.add(itembtn2)
        markup.add(itembtn3)
        msg = bot.send_message(
            message.chat.id, 'Выберите курс:', reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(msg, process_applyparametrs_step)
        global Usluga
        Usluga = message.text


def process_usluga_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        global Usluga
        Usluga = message.text
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        if message.text == 'Стрижки':
            msg = bot.send_message(
                chat_id, 'В какой половине дня Вам будет удобно?\n<b>Пример:</b> "В первой половине дня",\n"Во второй половине дня"', reply_markup=markup, parse_mode='html')
            bot.register_next_step_handler(msg, process_applyparametrs_step)
        elif message.text == 'Полировка':
            msg = bot.send_message(
                chat_id, 'В какой половине дня Вам будет удобно?\n<b>Пример:</b> "В первой половине дня",\n"Во второй половине дня"', reply_markup=markup)
            bot.register_next_step_handler(msg, process_applyparametrs_step)
        else:
            msg = bot.send_message(
                chat_id, 'Во сколько Вам нужно быть готовой?\n<b>Указать время:</b>\n<i>Пример:</i> "В 12-00 нужно быть готовой"', reply_markup=markup, parse_mode='html')
            bot.register_next_step_handler(msg, process_applyparametrs_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_applyparametrs_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        user = user_dict[chat_id]
        user.applyParam = message.text
        user.fullname = message.from_user.first_name + \
            ' ' + message.from_user.last_name
        if message.text == '🌟 Базовый экспресс-курс по причёскам 🌟':
            bot.send_message(
                chat_id, '<b>Программа курса :</b>', parse_mode='html')
            bot.send_photo(
                message.chat.id, open('images/kurs_3.jpg', 'rb'))

        elif message.text == '🌟 Свадебные прически 🌟':
            bot.send_message(
                chat_id, '<b>Программа курса :</b>', parse_mode='html')
            bot.send_photo(
                message.chat.id, open('images/kurs_1.jpg', 'rb'),)

        elif message.text == '🌟 Прически для себя 🌟':
            bot.send_message(
                chat_id, '<b>Программа курса :</b>', parse_mode='html')
            bot.send_photo(
                message.chat.id, open('images/kurs_2.jpg', 'rb'),)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(
            chat_id, 'Введите желаемую дату\nВ формате: День.Месяц.Год', reply_markup=markup)
        bot.register_next_step_handler(msg, process_date_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_date_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.dateZapis = message.text
        # markup_contact = types.ReplyKeyboardMarkup(
        #     resize_keyboard=True, row_width=2)
        # button_phone = types.KeyboardButton(
        #     text="Отправить номер телефона для быстрой записи", request_contact=True)
        # markup_contact.add(button_phone)
        msg = bot.send_message(
            chat_id, 'Введите ваш номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_phone_step(message):
    try:
        # int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Введите Instagram Ник:')
        bot.register_next_step_handler(msg, process_instagram_step)
        # print(user.phone)
    except Exception as e:
        msg = bot.reply_to(
            message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_phone_step)


def process_instagram_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.instagram = message.text
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(
            text='Подтвердить запись', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(
            text='Сбросить все и вернуться в главное меню', callback_data='no')
        keyboard.add(key_no)
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(
            user, 'Ваша заявка', message.from_user.first_name + ' ПОДТВЕРДИТЬ?'), reply_markup=keyboard, parse_mode="Markdown")
        bot.send_message(config.chat_id, getRegData(
            user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def getRegData(user, title, name):
    t = Template('$title *$name* \n Инстаграм Ник: *$instagram* \n ФИО: *$fullname* \n Телефон: *$phone* \n Услуга: *$Usluga* \n Желаемая дата: *$dateZapis* \n Дополнительные сведения: *$applyParam*')

    return t.substitute({
        'title': title,
        'name': name,
        'instagram': user.instagram,
        'fullname': user.fullname,
        'phone': user.phone,
        'Usluga': Usluga,
        'dateZapis': user.dateZapis,
        'applyParam': user.applyParam,
    })


# @bot.message_handler(content_types=['contact'])
# def hadle_contact(message):
#     try:
#         chat_id = message.chat.id
#         user_dict[chat_id] = User(message.text)
#         user = user_dict[chat_id]
#         user.phone = message.contact.phone_number

#         bot.send_message(message.from_user.id,
#                          f'Я получил твой контакт: {message.contact.phone_number}')
#         msg = bot.send_message(chat_id, 'Введите Instagram Ник:')
#         bot.register_next_step_handler(msg, process_instagram_step)
#         print(user.phone)
#     except Exception as e:
#         msg = bot.reply_to(
#             message, 'Вы не отправили номер телефона повторите попытку')
#         bot.register_next_step_handler(msg, hadle_contact)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    message = call.message
    user_dict[chat_id] = User(message.text)
    user = user_dict[chat_id]
    if call.data == "yes":
        bot.answer_callback_query(
            callback_query_id=call.id, show_alert=False, text="Подтверждено")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id, text='Спасибо! 📝 Ваша заявка на запись успешно отправлена 📝  \n Ожидайте с Вами свяжутся в ближайшее время 📞', reply_markup=None, parse_mode="html")
        social_buttoms(message)
    elif call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text="Следуйте инструкциям бота", reply_markup=None)
        send_welcome2(message)
        bot.answer_callback_query(
            callback_query_id=call.id, show_alert=False, text="Возврат")
# произвольный текст


def social_buttoms(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    btn1 = types.InlineKeyboardButton(
        text='🌍 Посетите мой Сайт 🌍', url="roihairstylist.top")  # кнопка «Да»
    keyboard.add(btn1)  # добавляем кнопку в клавиатуру
    btn2 = types.InlineKeyboardButton(
        text='📲 Instagram профиль 📳', url="roihairstylist.top")
    keyboard.add(btn2)
    btn3 = types.InlineKeyboardButton(
        text='📹 YouTube канал 📹', url="https://www.youtube.com/channel/UCGqUb8O0t_lg3x_0gE22TEg")
    keyboard.add(btn3)
    btn4 = types.InlineKeyboardButton(
        text='📩 Телеграм канал 📨', url="https://t.me/tanya_roi_hairstylist")
    keyboard.add(btn4)
    bot.send_message(message.chat.id,
                     'Так же меня можно найти перейдя по ссылкам ⬇', reply_markup=keyboard, parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(
        message.chat.id, 'Отправить заявку /start\nПомощь - /help')

# произвольное фото


@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
