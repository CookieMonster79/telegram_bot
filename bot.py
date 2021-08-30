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
    item2 = types.KeyboardButton('🎽 Узнаем курсы')
    item3 = types.KeyboardButton('🍩 Узнаем как система')
    item4 = types.KeyboardButton('🔱 Другое')

    markup.add(item1, item2, item3, item4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEC1MRhLOV2h34WtU_oXoQTZuUz2gIzSwACEgADPaRVGWRqgg9i5-QnIAQ')

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое к примеру давай глянем что у нас там по KS? /exchange.\n',
                     reply_markup=markup
                     )


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🎇 Рандомное число':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 100)))
        elif message.text == '🎽 Узнаем курсы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🎇 Курс Евро')
            item2 = types.KeyboardButton('🎽 Курс Доллара')
            back = types.KeyboardButton('◀ Назад')
            markup.add(item1, item2, back)

            bot.send_message(message.chat.id, '🎽 Узнаем курсы', reply_markup=markup)

        elif message.text == '🍩 Узнаем как система':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('👾 О боте')
            item2 = types.KeyboardButton('📦 Что в коробке?')
            back = types.KeyboardButton('◀ Назад')
            markup.add(item1, item2, back)

            bot.send_message(message.chat.id, '🍩 Узнаем как система', reply_markup=markup)

        elif message.text == '🔱 Другое':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Настройки')
            item2 = types.KeyboardButton('Подписка')
            item3 = types.KeyboardButton('🗿 Стикер')
            back = types.KeyboardButton('◀ Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message(message.chat.id, '🔱 Другое', reply_markup=markup)

        elif message.text == '◀ Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🎇 Рандомное число')
            item2 = types.KeyboardButton('🎽 Узнаем курсы')
            item3 = types.KeyboardButton('🍩 Узнаем как система')
            item4 = types.KeyboardButton('🔱 Другое')

            markup.add(item1, item2, item3, item4)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEC1MRhLOV2h34WtU_oXoQTZuUz2gIzSwACEgADPaRVGWRqgg9i5-QnIAQ')

            bot.send_message(message.chat.id,
                             '◀ Назад',
                             reply_markup=markup
                             )

        elif message.text == '🗿 Стикер':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEC1MxhLOp1Ts-f8Q3AVILqODevZf_TMwACgwYAAtJaiAFBGhO34v4iBCAE')


bot.polling(none_stop=True)
