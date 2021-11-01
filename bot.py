import random
from datetime import datetime

import psycopg2
import requests
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from tabulate import tabulate
from telebot import types
from telebot.types import KeyboardButton
from threading import Thread


import config

bot = telebot.TeleBot(config.TOKEN)

# Список идентификаторов пользователей кому доступен бот
list_user = ['moskva_max', 'Sasha6Popova']


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Начало работы бота
    :param message: сообщение из чата с пользователем
    :return: Возврат Сообщение с пользовательской клавиатурой
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎇 Рандомное число')
    item2 = types.KeyboardButton('🔮 Узнаем погоду')
    item3 = types.KeyboardButton('🍩 ITSM365')
    item4 = types.KeyboardButton('🔱 Другое')

    markup.add(item1, item2, item3, item4)

    def approvDate():
        text = 'Пусто'
        con = psycopg2.connect(
            database=config.PG_DATABASE,
            user=config.PG_USER,
            password=config.PG_PASSWORD,
            host=config.PG_HOST,
            port=config.PG_PORT
        )
        cur = con.cursor()
        cur.execute('SELECT text, year, dm from public."Birthday"')
        rows = cur.fetchall()
        curDate = datetime.now().strftime("%d-%m")
        curYear = datetime.now().strftime("%Y")
        for row in rows:
            if (row[2] == curDate):
                text = 'Сегодня ' + row[0] + ', ' + 'родился(-лась) ' + row[1] + ', лет ' + (int(curYear) - int(row[1]))
            else:
                text = 'Сегодня, нет ни у кого дня рождения!'

        con.close()
        return text

    def run():
        scheduler.add_job(bot.send_message, trigger='cron', hour='10', minute='00',
                      args=[message.chat.id, approvDate()])
        scheduler.add_job(bot.send_message, trigger='cron', hour='18', minute='53',
                          args=[message.chat.id, approvDate()])
        scheduler.add_job(bot.send_message, trigger='cron', hour='18', minute='54',
                          args=[message.chat.id, approvDate()])
        scheduler.start()

    thread = Thread(target=run())
    thread.start()

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое.\n',
                     reply_markup=markup
                     )


def toFixed(numObj, digits=0):
    """
    Удаляет символы после запятой
    :param numObj: входное значение
    :param digits: сколько символов оставить после запятой, если 0 то запятая убирается
    :return:
    """
    return f"{numObj:.{digits}f}"


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'})


@bot.message_handler(content_types=['text'])
def bot_message(message):
    e = 0
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
                item2 = types.KeyboardButton('📦 Заявок сегодня')
                item3 = types.KeyboardButton('📦 Стат. по клиентам')
                item4 = types.KeyboardButton('📦 Войти под ...')
                item5 = types.KeyboardButton('🚪 Проверить заявки')
                item6 = types.KeyboardButton('📦 Ещё одно 4')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, item3, item4, item5, item6, back)

                bot.send_message(message.chat.id, '🍩 ITSM365', reply_markup=markup)

            elif message.text == '🍀 Статус системы':
                try:
                    r = requests.get(f"{config.PATH}sd/services/rest/check-status")
                    data = r.text
                    time = toFixed(r.elapsed.total_seconds(), 2)

                    bot.send_message(message.chat.id,
                                     f"Ответ сервера: {data}\n" +
                                     f"Время запроса: {time} сек")

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '📦 Заявок сегодня':
                try:
                    url = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                    files = [
                        ('script', ('countCall.groovy', open('Groovy Script/countCall.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = {
                        'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
                        'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
                    }

                    response = requests.request("POST", url, headers=headers, data={}, files=files)

                    data = response.text

                    bot.send_message(message.chat.id,
                                     f"{data}")
                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '📦 Стат. по клиентам':
                '''
                !!!!!!!!Переписать статистику по клиентам под вывод на телефон'''
                try:
                    url = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                    files = [
                        ('script', ('countCall.groovy', open('Groovy Script/tableStatisticForClient.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = {
                        'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
                        'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
                    }

                    response = requests.request("POST", url, headers=headers, data={}, files=files)

                    data = response.text

                    data = data.replace("]", "")
                    data = data.replace("[", "")
                    data = data.replace(" ", "")
                    result = data.split(",")

                    def split_list(alist, wanted_parts=1):
                        length = len(alist)
                        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                                for i in range(wanted_parts)]

                    lists = split_list(result, wanted_parts=9)
                    lenght = len(lists)

                    table = {}

                    for i in range(lenght):
                        pool = lists[i]
                        table[i] = pool

                    headers = ["Название", "Заявки", "Сотрудники", "Регл. работы"]

                    text_mess = tabulate(
                        [table[0]  # , table[1], table[2], table[3], table[4], table[5], table[6], table[7], table[8]
                         ],
                        headers)

                    bot.send_message(message.chat.id,
                                     text_mess, parse_mode="HTML")
                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '📦 Войти под ...':
                try:
                    markup = types.ForceReply(selective=False)
                    bot.send_message(message.chat.id, f"Введите Фамилию, типа Иванов", reply_markup=markup)

                    @bot.message_handler(content_types=['text'])
                    def message_input_step(message_user):
                        global user_text
                        user_text = message_user.text

                        if user_text != '':
                            with open('Groovy Script/loginForEmpl.groovy', 'r', encoding="utf-8") as f:
                                old_data = f.read()

                            new_data = old_data.replace('Иванов', user_text)

                            with open('Groovy Script/loginForEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data)

                            url_ACCESSKEY = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                            files = [
                                ('script', ('loginForEmpl.groovy', open('Groovy Script/loginForEmpl.groovy', 'rb'),
                                            'application/octet-stream'))
                            ]
                            headers = {
                                'Authorization': 'Basic UnVkb21hbkRTQE1PUy5QT0xVUy5HTEQ6MTIz',
                                'Cookie': 'JSESSIONID=F6142A7BA1F133CF7C2AFC77DB5D8BA6'
                            }

                            response = requests.request("POST", url_ACCESSKEY, headers=headers, data={}, files=files)

                            data = response.text

                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('🍀 Статус системы')
                            item2 = types.KeyboardButton('📦 Заявок сегодня')
                            item3 = types.KeyboardButton('📦 Стат. по клиентам')
                            item4 = types.KeyboardButton('📦 Войти под ...')
                            item5 = types.KeyboardButton('📦 Ещё одно 3')
                            item6 = types.KeyboardButton('📦 Ещё одно 4')
                            back: KeyboardButton = types.KeyboardButton('◀ Назад')
                            markup.add(item1, item2, item3, item4, item5, item6, back)

                            bot.send_message(message.chat.id, text=data, parse_mode="HTML", reply_markup=markup)

                            new_data2 = new_data.replace(user_text, 'Иванов')
                            with open('Groovy Script/loginForEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data2)

                    bot.register_next_step_handler(message,
                                                   message_input_step)
                    # добавляем следующий шаг, перенаправляющий пользователя на message_input_step
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

            elif message.text == '🚪 Проверить заявки':
                bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')
                # try:

            # except:
            #    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

            elif message.text == '🔱 Другое':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🛠️ Настройка напоминаний')
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

            elif message.text == '🛠️ Настройка напоминаний':
                try:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item2 = types.KeyboardButton('📍 Запуск планировщика')
                    item3 = types.KeyboardButton('🗒️ Все даты')
                    back = types.KeyboardButton('◀ Назад')
                    markup.add(item2, item3, back)

                    bot.send_message(message.chat.id, '🛠️ Настройка напоминаний', reply_markup=markup)

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '🗒️ Все даты':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item2 = types.KeyboardButton('📍 Запуск планировщика')
                item3 = types.KeyboardButton('🗒️ Все даты')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item2, item3, back)

                try:
                    con = psycopg2.connect(
                        database=config.PG_DATABASE,
                        user=config.PG_USER,
                        password=config.PG_PASSWORD,
                        host=config.PG_HOST,
                        port=config.PG_PORT
                    )

                    cur = con.cursor()
                    cur.execute('SELECT * FROM public."Birthday"')
                    rows = cur.fetchall()

                    for row in rows:
                        bot.send_message(message.chat.id, parse_mode="HTML", text=
                        "Описание: " + row[0] + "<pre>\n</pre> Год рождения: " +
                        row[1] + "<pre>\n</pre> День и месяц: " + row[2])

                    con.close()

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(', reply_markup=markup)

            elif message.text == '🗿 Стикер':
                try:
                    i = random.randint(1, 100)

                    con = psycopg2.connect(
                        database=config.PG_DATABASE,
                        user=config.PG_USER,
                        password=config.PG_PASSWORD,
                        host=config.PG_HOST,
                        port=config.PG_PORT
                    )

                    cur = con.cursor()

                    cur.execute('SELECT * FROM public."Stickers" WHERE id = ' + str(i))

                    rows = cur.fetchall()

                    for row in rows:
                        bot.send_sticker(message.chat.id, row[1])

                    con.close()

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '🏤 Москва':
                try:
                    r = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q=moscow&appid={config.WEATHER_TOKEN}&units=metric"
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
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '🚣 Санкт-Петербург':
                try:
                    r = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&appid={config.WEATHER_TOKEN}&units=metric"
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
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

    else:
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
