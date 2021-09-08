import random

import requests
import telebot
from telebot import types

import config
from config import WEATHER_TOKEN, PATH, ACCESSKEY

bot = telebot.TeleBot(config.TOKEN)


# Для тестирования - эхо функция
# @bot.message_handler(content_types=['text'])
# def lalala(message):
#    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎇 Рандомное число')
    item2 = types.KeyboardButton('🔮 Узнаем погоду')
    item3 = types.KeyboardButton('🍩 ITSM365')
    item4 = types.KeyboardButton('🔱 Другое')

    markup.add(item1, item2, item3, item4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEC1MRhLOV2h34WtU_oXoQTZuUz2gIzSwACEgADPaRVGWRqgg9i5-QnIAQ')

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое.\n',
                     reply_markup=markup
                     )


# Список идентификаторов пользователей кому доступен бот
list_user = ['moskva_max', 'Sasha6Popova']


# Функция для отсечения символов после запятой

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.username in list_user:
        if message.chat.type == 'private':
            if message.text == '🎇 Рандомное число':
                bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 100)))
            elif message.text == '🔮 Узнаем погоду':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🏤 Москва')
                item2 = types.KeyboardButton('🚣 Санкт-Петербург')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, back)

                bot.send_message(message.chat.id, '🔮 Узнаем погоду', reply_markup=markup)

            elif message.text == '🍩 ITSM365':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🍀 Статус системы')
                item2 = types.KeyboardButton('📦 Количество заявок сегодня')
                item3 = types.KeyboardButton('📦 Статистика по клиентам')
                item4 = types.KeyboardButton('📦 Ещё одно 2')
                item5 = types.KeyboardButton('📦 Ещё одно 3')
                item6 = types.KeyboardButton('📦 Ещё одно 4')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, item3, item4, item5, item6, back)

                bot.send_message(message.chat.id, '🍩 ITSM365', reply_markup=markup)

            elif message.text == '🍀 Статус системы':
                try:
                    r = requests.get(f"{PATH}sd/services/rest/check-status")
                    data = r.text
                    time = toFixed(r.elapsed.total_seconds(), 2)

                    bot.send_message(message.chat.id,
                                     f"Ответ сервера: {data}\n" +
                                     f"Время запроса: {time} сек")

                except:
                    bot.send_message('Что-то пошло не по плану :(')

            elif message.text == '📦 Количество заявок сегодня':
                try:
                    url = f"{PATH}sd/services/rest/exec?accessKey={ACCESSKEY}"

                    payload = {}
                    files = [
                        ('script', ('countCall.groovy', open('Groovy Script/countCall.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = {
                        'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
                        'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload, files=files)

                    data = response.text

                    bot.send_message(message.chat.id,
                                     f"{data} заявки")
                except:
                    bot.send_message('Что-то пошло не по плану :(')

            elif message.text == '📦 Статистика по клиентам':
                try:
                    url = f"{PATH}sd/services/rest/exec?accessKey={ACCESSKEY}"

                    payload = {}
                    files = [
                        ('script', ('countCall.groovy', open('Groovy Script/tableStatisticForClient.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = {
                        'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
                        'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload, files=files)

                    data = response.text

                    bot.send_message(message.chat.id,
                                     f"{data}")
                except:
                    bot.send_message('Что-то пошло не по плану :(')

            elif message.text == '🔱 Другое':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Настройки')
                item3 = types.KeyboardButton('🗿 Стикер')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item3, back)

                bot.send_message(message.chat.id, '🔱 Другое', reply_markup=markup)

            elif message.text == '◀ Назад':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🎇 Рандомное число')
                item2 = types.KeyboardButton('🔮 Узнаем погоду')
                item3 = types.KeyboardButton('🍩 ITSM365')
                item4 = types.KeyboardButton('🔱 Другое')

                markup.add(item1, item2, item3, item4)

                bot.send_message(message.chat.id,
                                 '◀ Назад',
                                 reply_markup=markup
                                 )

            elif message.text == '🗿 Стикер':
                check = random.randint(0, 10)
                if check == 0:
                    bot.send_sticker(message.chat.id,
                                     'CAACAgIAAxkBAAEC1MxhLOp1Ts-f8Q3AVILqODevZf_TMwACgwYAAtJaiAFBGhO34v4iBCAE')
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

            elif message.text == '🏤 Москва':
                try:
                    r = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q=moscow&appid={WEATHER_TOKEN}&units=metric"
                    )
                    data = r.json()

                    cur_weat = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    pressure = data["main"]["pressure"]
                    wind = data["wind"]["speed"]

                    bot.send_message(message.chat.id,
                                     f"Температура: {cur_weat}C°\nВлажность: {humidity}%\n"
                                     f"Давление: {pressure} мм.рт.ст.\nВетер: {wind} м/сек\n")


                except:
                    bot.send_message('Что-то пошло не по плану :(')

            elif message.text == '🚣 Санкт-Петербург':
                try:
                    r = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&appid={WEATHER_TOKEN}&units=metric"
                    )
                    data = r.json()

                    cur_weat = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    pressure = data["main"]["pressure"]
                    wind = data["wind"]["speed"]

                    bot.send_message(message.chat.id,
                                     f"Температура: {cur_weat}C°\nВлажность: {humidity}%\n"
                                     f"Давление: {pressure} мм.рт.ст.\nВетер: {wind} м/сек\n")


                except:
                    bot.send_message('Что-то пошло не по плану :(')
    else:
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
