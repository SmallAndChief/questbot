from telebot import TeleBot, types
from data import install_users_data, save_users_data, install_quest

quest = install_quest()
users_data = install_users_data()

TOKEN = ""

bot = TeleBot(token=TOKEN)

bot.set_my_commands([types.BotCommand('start', 'начало работы'),
                     types.BotCommand('help', 'помощь'),
                     types.BotCommand('quest', 'начать квест'),
                     types.BotCommand('restart', 'сброс квеста')])

help_button = types.KeyboardButton("/help")
quest_button = types.KeyboardButton("/quest")
reset_button = types.KeyboardButton("/restart")


def quest_message(user_id, chat_id):
    if user_id not in users_data.keys():
        users_data[user_id] = 'start'
    user_loc = quest[users_data[user_id]]
    text = user_loc['description']
    with open(user_loc["image"], 'rb') as photo:
        if 'options' in user_loc.keys():
            markup = types.InlineKeyboardMarkup()
            markup.row_width = 2
            markup.add(types.InlineKeyboardButton('1', callback_data=user_loc['options']["1"]),
                       types.InlineKeyboardButton('2', callback_data=user_loc['options']["2"]),
                       types.InlineKeyboardButton('3', callback_data=user_loc['options']["3"]))
            bot.send_photo(chat_id=chat_id, photo=photo, caption=text, reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(help_button, reset_button)
            bot.send_photo(chat_id=chat_id, photo=photo, caption=text, reply_markup=markup)
    save_users_data(users_data)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(help_button, quest_button)
    bot.send_message(chat_id=message.chat.id,
                     text='''Приветствую вас в боте-квесте "Исследование затеряного города"!
                          \nВведите /help для инструкции или /quest для начала квеста.''',
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(reset_button, quest_button)
    bot.send_message(chat_id=message.chat.id,
                     text='Для начала квеста введите /quest. Введите /restart для сброса квеста',
                     reply_markup=markup)


@bot.message_handler(commands=['restart'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(help_button, quest_button)
    users_data[str(message.from_user.id)] = 'start'
    bot.send_message(chat_id=message.chat.id,
                     text='Квест сброшен. Для начала квеста введите /quest.',
                     reply_markup=markup)
    save_users_data(users_data)


@bot.message_handler(commands=['quest'])
def start_quest_message(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    quest_message(user_id, chat_id)


@bot.callback_query_handler(func=lambda call: True)
def quest_next(call):
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)
    users_data[str(user_id)] = call.data
    quest_message(user_id, chat_id)


@bot.message_handler(content_types=['text'])
def text_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(help_button, quest_button)
    bot.send_message(chat_id=message.chat.id,
                     text='Я не понимаю чего вы хотите. Введите /help.',
                     reply_markup=markup)


bot.polling()
