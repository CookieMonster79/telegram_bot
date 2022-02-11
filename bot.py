import random
from datetime import datetime

import prettytable as pt
import psycopg2
import requests
import schedule
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from tabulate import tabulate
from telebot import types
from telebot.types import KeyboardButton
from threading import Thread

import config

bot = telebot.TeleBot(config.TOKEN)

# Список идентификаторов пользователей кому доступен бот
list_user = ['moskva_max', 'Sa_Mosk']


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

    def approvedDate():
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
            if row[2] == curDate:
                text = 'Сегодня ' + row[0] + ', ' + 'родился(-лась) ' + row[1] + ', лет ' + (int(curYear) - int(row[1]))
            else:
                text = 'Сегодня, нет ни у кого дня рождения!'

        con.close()
        return text

    def run():
        if len(scheduler.get_jobs()) == 0:
            scheduler.add_job(bot.send_message, trigger='cron', hour='10', minute='00',
                              args=[message.chat.id, approvedDate()])
            scheduler.start()

    thread = Thread(target=run())
    thread.start()

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое.\n' +
                     'Сейчас например запустил планировщик, теперь каждый день в 10:00 будут приходить сообщения.\n',
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
                    headers = config.headers

                    response = requests.request("POST", url, headers=headers, data={}, files=files)

                    data = response.text

                    bot.send_message(message.chat.id,
                                     f"{data}")
                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '📦 Стат. по клиентам':

                try:
                    url = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                    files = [
                        ('script', ('countCall.groovy', open('Groovy Script/tableStatisticForClient.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = config.headers

                    response = requests.request("POST", url, headers=headers, data={}, files=files)

                    list = []
                    data = response.text
                    data = data.replace("]", "", 1)
                    data = data.replace("[", "", 1)

                    for i in range(0, 1):
                        list.extend(data.split(', '))

                    table = pt.PrettyTable(["Название", "Заявки", "Сотрудники", "Регл. работы"])
                    table.align['Название'] = 'l'
                    table.align['Заявки'] = 'r'
                    table.align['Сотрудники'] = 'r'
                    table.align['Регл. работы'] = 'r'

                    '''
                    Переписать формирование выводящий таблицы под цикл, пробовал ниже пока не получилось
                    data = []
                    for j in range(0, len(list), 4):
                        a1 = (f'{list[j]}', list[j+1], list[j+2], list[j+3])
                        data.append(a1)
                    '''

                    data = [
                        (f'{list[0]}', int(list[1]), int(list[2]), int(list[3])),
                        (f'{list[4]}', int(list[5]), int(list[6]), int(list[7])),
                        (f'{list[8]}', int(list[9]), int(list[10]), int(list[11])),
                        (f'{list[12]}', int(list[13]), int(list[14]), int(list[15])),
                        (f'{list[16]}', int(list[17]), int(list[18]), int(list[19])),
                        (f'{list[20]}', int(list[21]), int(list[22]), int(list[23])),
                        (f'{list[24]}', int(list[25]), int(list[26]), int(list[27])),
                        (f'{list[28]}', int(list[29]), int(list[30]), int(list[31])),
                        (f'{list[32]}', int(list[33]), int(list[34]), int(list[35])),
                        (f'{list[36]}', int(list[37]), int(list[38]), int(list[39])),
                        (f'{list[40]}', int(list[41]), int(list[42]), int(list[43])),
                        (f'{list[44]}', int(list[45]), int(list[46]), int(list[47])),
                        (f'{list[48]}', int(list[49]), int(list[50]), int(list[51])),
                    ]

                    for name, call, emp, regalement in data:
                        table.add_row([name, f'{call:.0f}', f'{emp:.0f}', f'{regalement:.0f}'])

                    bot.send_message(message.chat.id,
                                     f'<pre>{table}</pre>', parse_mode="HTML")
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
                            headers = config.headers

                            responseNSD = requests.request("POST", url_ACCESSKEY, headers=headers, data={}, files=files)

                            dataResponse = responseNSD.text

                            markupKeybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1Button = types.KeyboardButton('🍀 Статус системы')
                            item2Button = types.KeyboardButton('📦 Заявок сегодня')
                            item3Button = types.KeyboardButton('📦 Стат. по клиентам')
                            item4Button = types.KeyboardButton('📦 Войти под ...')
                            item5Button = types.KeyboardButton('📦 Ещё одно 3')
                            item6Button = types.KeyboardButton('📦 Ещё одно 4')
                            backButton: KeyboardButton = types.KeyboardButton('◀ Назад')
                            markupKeybord.add(item1Button, item2Button, item3Button, item4Button, item5Button,
                                              item6Button, backButton)

                            bot.send_message(message.chat.id, text=dataResponse, parse_mode="HTML",
                                             reply_markup=markupKeybord)

                            new_data2 = new_data.replace(user_text, 'Иванов')
                            with open('Groovy Script/loginForEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data2)

                    bot.register_next_step_handler(message,
                                                   message_input_step)
                    # добавляем следующий шаг, перенаправляющий пользователя на message_input_step
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

            elif message.text == '🚪 Проверить заявки':
                try:
                    markup = types.ForceReply(selective=False)
                    bot.send_message(message.chat.id, f"Введите Фамилию, типа Петров", reply_markup=markup);

                    @bot.message_handler(content_types=['text'])
                    def message_input_step(message_user):
                        global user_text
                        user_text = message_user.text

                        if user_text != '':
                            with open('Groovy Script/SClistEmpl.groovy', 'r', encoding="utf-8") as f:
                                old_data = f.read()

                            new_data = old_data.replace('Иванов', user_text)

                            with open('Groovy Script/SClistEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data)

                            url_ACCESSKEY = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                            files = [
                                ('script', ('SClistEmpl.groovy', open('Groovy Script/SClistEmpl.groovy', 'rb'),
                                            'application/octet-stream'))
                            ]
                            headers = config.headers

                            responseNSD = requests.request("POST", url_ACCESSKEY, headers=headers, data={}, files=files)

                            # Возвращаем файл как было
                            new_data2 = new_data.replace(user_text, 'Иванов')
                            with open('Groovy Script/SClistEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data2)

                            dataResponse = responseNSD.text.replace("[", "", 1)
                            dataResponse = dataResponse.replace("]", "", 1)

                            markupKeybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1Button = types.KeyboardButton('🍀 Статус системы')
                            item2Button = types.KeyboardButton('📦 Заявок сегодня')
                            item3Button = types.KeyboardButton('📦 Стат. по клиентам')
                            item4Button = types.KeyboardButton('📦 Войти под ...')
                            item5Button = types.KeyboardButton('🚪 Проверить заявки')
                            item6Button = types.KeyboardButton('📦 Ещё одно 4')
                            backButton: KeyboardButton = types.KeyboardButton('◀ Назад')

                            markupKeybord.add(item1Button, item2Button, item3Button, item4Button, item5Button,
                                              item6Button, backButton)

                            if dataResponse != '':
                                list_empl = dataResponse.split('=')

                                for k in range(0, len(list_empl)):
                                    list_empl[k] = list_empl[k].replace('{', '')
                                    list_empl[k] = list_empl[k].replace('}', '')
                                    list_empl[k] = list_empl[k].replace('[', '')
                                    list_empl[k] = list_empl[k].replace(']', '')

                                list_call_title = list_empl[2].split(',')
                                list_call_UUID = list_empl[3].split(',')

                                # Формируется Inline клавиатура
                                InlineKeyboardMarkup = types.InlineKeyboardMarkup()

                                if list_call_title[0] != '':
                                    for j in range(0, len(list_call_title) - 1, 5):
                                        if (len(list_call_title) - j) > 5:
                                            button1 = types.InlineKeyboardButton(url=config.PATH + 'sd/operator/#uuid:' +
                                                                                     list_call_UUID[j], text=list_call_title[j])
                                            button2 = types.InlineKeyboardButton(url=config.PATH + 'sd/operator/#uuid:' +
                                                                                     list_call_UUID[j + 1],
                                                                                 text=list_call_title[j + 1])
                                            button3 = types.InlineKeyboardButton(url=config.PATH + 'sd/operator/#uuid:' +
                                                                                     list_call_UUID[j + 2],
                                                                                 text=list_call_title[j + 2])
                                            button4 = types.InlineKeyboardButton(url=config.PATH + 'sd/operator/#uuid:' +
                                                                                     list_call_UUID[j + 3],
                                                                                 text=list_call_title[j + 3])
                                            button5 = types.InlineKeyboardButton(url=config.PATH + 'sd/operator/#uuid:' +
                                                                                     list_call_UUID[j + 4],
                                                                                 text=list_call_title[j + 4])
                                            InlineKeyboardMarkup.row(button1, button2, button3, button4, button5)
                                        else:
                                            for l in range(0, len(list_call_title) - j):
                                                if len(list_call_title) - j == 1:
                                                    button1 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l], text=list_call_title[l])
                                                    InlineKeyboardMarkup.row(button1)
                                                elif len(list_call_title) - j == 2:
                                                    button1 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l], text=list_call_title[l])
                                                    button2 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l+1], text=list_call_title[l+1])
                                                    InlineKeyboardMarkup.row(button1, button2)
                                                elif len(list_call_title) - j == 3:
                                                    button1 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l], text=list_call_title[l])
                                                    button2 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l+1], text=list_call_title[l+1])
                                                    button3 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l+2], text=list_call_title[l+2])
                                                    InlineKeyboardMarkup.row(button1, button2, button3)
                                                elif len(list_call_title) - j == 4:
                                                    button1 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l], text=list_call_title[l])
                                                    button2 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l+1], text=list_call_title[l+1])
                                                    button3 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l+2], text=list_call_title[l+2])
                                                    button4 = types.InlineKeyboardButton(
                                                        url=config.PATH + 'sd/operator/#uuid:' +
                                                            list_call_UUID[l + 3], text=list_call_title[l + 3])
                                                    InlineKeyboardMarkup.row(button1, button2, button3, button4)

                                bot.send_message(message.chat.id, text='Заявки сотрудника' + list_empl[0], parse_mode="HTML",
                                                 reply_markup=InlineKeyboardMarkup)

                                bot.send_message(message.chat.id, text='Закончил вывод заявок!', parse_mode="HTML",
                                                 reply_markup=markupKeybord)
                            else:
                                bot.send_message(message.chat.id, text='Сотрудник не найден!', parse_mode="HTML",
                                                 reply_markup=markupKeybord)

                    bot.register_next_step_handler(message,
                                                   message_input_step)

                    # добавляем следующий шаг, перенаправляющий пользователя на message_input_step
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

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
                        bot.send_message(message.chat.id, parse_mode="HTML",
                                         text="Описание: " + row[0] + "<pre>\n</pre> Год рождения: " +
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
                        f"http://api.openweathermap.org/data/2.5/weather?q=moscow&appid="
                        f"{config.WEATHER_TOKEN}&units=metric"
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
                        f"http://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&appid="
                        f"{config.WEATHER_TOKEN}&units=metric"
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
