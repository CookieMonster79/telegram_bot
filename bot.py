import random

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)

####WEATHER_TOKEN

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
                     'Умею всякое.\n',
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

            bot.send_message(message.chat.id,
                             '◀ Назад',
                             reply_markup=markup
                             )

        elif message.text == '🗿 Стикер':
            check = random.randint(0, 10)
            if check == 0:
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEC1MxhLOp1Ts-f8Q3AVILqODevZf_TMwACgwYAAtJaiAFBGhO34v4iBCAE')
            elif check == 1:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1NFhLPLWs4U5iYVxC-47uKej0iWnYgACJoEAAp7OCwABft37e18RdUQgBA')
            elif check == 2:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1NNhLPLlGucRbNjwJerrAq_ga4RKDgACP4EAAp7OCwABat5BLJOatCEgBA')
            elif check == 3:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1NVhLPLyk1nwyfbAzEv05BU5maeZvAACQwADpm6pHZcs4TRf5iaYIAQ')
            elif check == 4:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1NlhLPL-KdUBui6RonmVWFGHesEFIwACXQADpm6pHUOQkUhEvjF7IAQ')
            elif check == 5:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1NthLPMKRdKkG3EXgsP2xhQtX4hRHwACzwkAAgi3GQLdwOHA1H1MIiAE')
            elif check == 6:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1N1hLPMXiQ7WTpKQEEDCTM6TQHC6zAACCgADPaRVGT4ahXGzmh7aIAQ')
            elif check == 7:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1N9hLPMjQmmMevHFmXDmLeCcZqmUOwAC5AcAApb6EgUSPp93kc5MGSAE')
            elif check == 8:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1OFhLPMsOA2G78uk-qZn1ww_y-MhEAAC7gcAApb6EgUV_ytCQwThRiAE')
            elif check == 9:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1ONhLPM2PXxQ-xzRdQo_bcD6Njo98QACFwADiwTqG-wbcBkhqTt9IAQ')
            elif check == 10:
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEC1OVhLPNAMfr9N1aPGXfxopPr0OxOngACJwADGELuCMj8_JJUedksIAQ')


bot.polling(none_stop=True)
