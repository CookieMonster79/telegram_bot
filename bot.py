import random

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


# Для тестирования
# @bot.message_handler(content_types=['text'])
# def lalala(message):
#    bot.send_message(message.chat.id, message.text)


# start - общая информация
# ks - перейти к просмотру ks
#
#
#


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎇 Рандомное число')
    item2 = types.KeyboardButton('🎽 Кнопка 1')
    item3 = types.KeyboardButton('🍩 Кнопка 2')
    item4 = types.KeyboardButton('🍟 Кнопка 3')

    markup.add(item1, item2, item3, item4)
    #    sti = open('static/start.webp', 'rb')
    #    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое к примеру давай глянем что у нас там по KS? /exchange.\n' +
                     'Чтобы получить помощь, нажмите /help.',
                     reply_markup=markup
                     )


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🎇 Рандомное число':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 100)))
    elif message.text == '🎽 Кнопка 1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('🎇 Курс Евро')
        item2 = types.KeyboardButton('🎽 Курс Доллара')
        back = types.KeyboardButton('◀ Назад')
        markup.add(item1, item2, back)

        bot.send_message(message.chat.id, 'Привет!.\n', reply_markup=markup)


bot.polling(none_stop=True)
