import json
import random
import time
from datetime import datetime

import prettytable as pt
import psycopg2
import requests
from multiprocessing.context import Process
import schedule
import telebot
from telebot import types
from telebot.types import KeyboardButton

import config

bot = telebot.TeleBot(config.TOKEN)
user_id = 240170832 #Данные ИД мой, нужно поудмать над тем чтобы изменить под message id

# Список идентификаторов пользователей кому доступен бот
list_user = ['moskva_max', 'Sa_Mosk']


def approvedDate():
    """
    Проверяет есть ли сегодня у кого-нибудь день рождение
    :return: Текст
    """
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
    # for row in rows:
    #     if row[2] == curDate:
    #     text = 'Сегодня ' + row[0] + ', ' + 'родился(-лась) ' + row[1] + ', лет ' + (int(curYear) - int(row[1]))
    #  else:
    #       text = 'Сегодня, нет ни у кого дня рождения!'

    con.close()
    return text


def send_message1():
    bot.send_message(chat_id=user_id, text='Планировщик успешно работает. Всё нормально!')


schedule.every().day.at('12:00').do(send_message1) #Тестовый ежедневный запуск отправки сообщения


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
    # item3 = types.KeyboardButton('🍩 ITSM365')
    item4 = types.KeyboardButton('🌬️ Алиса')
    item5 = types.KeyboardButton('🔱 Другое')

    # markup.add(item1, item2, item3, item4, item5)
    markup.row(item1, item2)
    markup.row(item4, item5)

    bot.send_message(message.chat.id,
                     'Привет!.\n' +
                     'Умею всякое.\n',
                     reply_markup=markup
                     )


def state_dev(id_dev):
    '''Функция получает состояние устройства если возвращается True, то включено'''
    url = f'https://api.iot.yandex.net/v1.0/devices/{id_dev}'

    payload = {}
    headers = {
        'Authorization': f'Bearer {config.TOKEN_YA}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    a = json.loads(response.text.replace("'", '"'))
    item = a.get('type')

    if item == 'devices.types.light': # написано условие для люстры следует переписать на конкретную группу в будущем
        return a.get('capabilities')[1].get('state').get('value')
    else:
        return a.get('capabilities')[0].get('state').get('value')


def run_scen(id_scen):
    '''Функция исполняет сценарий по id'''
    url = f'https://api.iot.yandex.net/v1.0/scenarios/{id_scen}/actions'

    payload = {}

    headers = {
        'Authorization': f'Bearer {config.TOKEN_YA}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def toFixed(numObj, digits=0):
    """
    Удаляет символы после запятой
    :param numObj: входное значение
    :param digits: сколько символов оставить после запятой, если 0 то запятая убирается
    :return:
    """
    return f"{numObj:.{digits}f}"


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.username in list_user:
        if message.chat.type == 'private':

            if message.text == '🎇 Рандомное число':
                bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 100)))

            elif message.text == '🍩 ITSM365':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🍀 Статус системы')
                item2 = types.KeyboardButton('📦 Заявок сегодня')
                item3 = types.KeyboardButton('📦 Стат. по клиентам')
                item4 = types.KeyboardButton('📦 Войти под ...')
                item5 = types.KeyboardButton('🚪 Заявки сотрудника')
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

                    response = requests.request("POST", url, headers=config.headers, data={}, files=files)

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

                    response = requests.request("POST", url, headers=config.headers, data={}, files=files)

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

                            responseNSD = requests.request("POST", url_ACCESSKEY, headers=config.headers, data={},
                                                           files=files)

                            markupKeybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1Button = types.KeyboardButton('🍀 Статус системы')
                            item2Button = types.KeyboardButton('📦 Заявок сегодня')
                            item3Button = types.KeyboardButton('📦 Стат. по клиентам')
                            item4Button = types.KeyboardButton('📦 Войти под ...')
                            item5Button = types.KeyboardButton('🚪 Заявки сотрудника')
                            item6Button = types.KeyboardButton('📦 Ещё одно 4')
                            backButton: KeyboardButton = types.KeyboardButton('◀ Назад')
                            markupKeybord.add(item1Button, item2Button, item3Button, item4Button, item5Button,
                                              item6Button, backButton)

                            bot.send_message(message.chat.id, text=responseNSD.text, parse_mode="HTML",
                                             reply_markup=markupKeybord)

                            # Меняем обратно значение в файле для правильного последующего использования
                            new_data2 = new_data.replace(user_text, 'Иванов')
                            with open('Groovy Script/loginForEmpl.groovy', 'w', encoding="utf-8") as f:
                                f.write(new_data2)

                    bot.register_next_step_handler(message, message_input_step)
                    # добавляем следующий шаг, перенаправляющий пользователя на message_input_step
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

            elif message.text == '🚪 Заявки сотрудника':
                try:
                    markup = types.ForceReply(selective=False)
                    bot.send_message(message.chat.id, f"Введите Фамилию, типа Петров", reply_markup=markup)

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

                            responseNSD = requests.request("POST", url_ACCESSKEY, headers=config.headers, data={},
                                                           files=files)

                            # Возвращаем Фамилию в файле, как было
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
                            item5Button = types.KeyboardButton('🚪 Заявки сотрудника')
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
                                if list_call_title[-1] == ' UUID':
                                    list_call_title = list_call_title[0:-1]
                                elif list_call_UUID[-1].isalpha():
                                    list_call_UUID = list_call_UUID[0:-1]

                                # Формируется Inline клавиатура
                                InlineKeyboardMarkup = types.InlineKeyboardMarkup()

                                if list_call_title[0] != '':
                                    len_call_final = len(list_call_title) % 5
                                    len_call_base = len(list_call_title) - len_call_final
                                    # Итерируемся по размерности заявок кратное 5 (если 10, то 2 раза)
                                    for j in range(0, len_call_base - 1, 5):
                                        if (len(list_call_title) - j) > 5:
                                            button1 = types.InlineKeyboardButton(
                                                url=config.PATH + 'sd/operator/#uuid:' +
                                                    list_call_UUID[j], text=list_call_title[j])
                                            button2 = types.InlineKeyboardButton(
                                                url=config.PATH + 'sd/operator/#uuid:' +
                                                    list_call_UUID[j + 1], text=list_call_title[j + 1])
                                            button3 = types.InlineKeyboardButton(
                                                url=config.PATH + 'sd/operator/#uuid:' +
                                                    list_call_UUID[j + 2], text=list_call_title[j + 2])
                                            button4 = types.InlineKeyboardButton(
                                                url=config.PATH + 'sd/operator/#uuid:' +
                                                    list_call_UUID[j + 3], text=list_call_title[j + 3])
                                            button5 = types.InlineKeyboardButton(
                                                url=config.PATH + 'sd/operator/#uuid:' +
                                                    list_call_UUID[j + 4], text=list_call_title[j + 4])
                                            InlineKeyboardMarkup.row(button1, button2, button3, button4, button5)
                                    # Итерируемся один раз для вывода остатка полученных заявок
                                    if len_call_final != 0:
                                        for l in range(0, 1):

                                            if len_call_final == 1:
                                                button1 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l],
                                                    text=list_call_title[len_call_base + l])
                                                InlineKeyboardMarkup.row(button1)

                                            elif len_call_final == 2:
                                                button1 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l],
                                                    text=list_call_title[len_call_base + l])
                                                button2 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 1],
                                                    text=list_call_title[len_call_base + l + 1])
                                                InlineKeyboardMarkup.row(button1, button2)

                                            elif len_call_final == 3:
                                                button1 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l],
                                                    text=list_call_title[len_call_base + l])
                                                button2 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 1],
                                                    text=list_call_title[len_call_base + l + 1])
                                                button3 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 2],
                                                    text=list_call_title[len_call_base + l + 2])
                                                InlineKeyboardMarkup.row(button1, button2, button3)

                                            elif len_call_final == 4:
                                                button1 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l],
                                                    text=list_call_title[len_call_base + l])
                                                button2 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 1],
                                                    text=list_call_title[len_call_base + l + 1])
                                                button3 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 2],
                                                    text=list_call_title[len_call_base + l + 2])
                                                button4 = types.InlineKeyboardButton(
                                                    url=config.PATH + 'sd/operator/#uuid:' +
                                                        list_call_UUID[len_call_base + l + 3],
                                                    text=list_call_title[len_call_base + l + 3])
                                                InlineKeyboardMarkup.row(button1, button2, button3, button4)

                                bot.send_message(message.chat.id, text='Заявки сотрудника: ' + list_empl[0],
                                                 parse_mode="HTML",
                                                 reply_markup=InlineKeyboardMarkup)

                                bot.send_message(message.chat.id, text='Закончил вывод заявок!', parse_mode="HTML",
                                                 reply_markup=markupKeybord)
                            else:
                                bot.send_message(message.chat.id, text='Сотрудник не найден!', parse_mode="HTML",
                                                 reply_markup=markupKeybord)

                    bot.register_next_step_handler(message, message_input_step)
                    # добавляем следующий шаг, перенаправляющий пользователя на message_input_step
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не по плану :(')

            elif message.text == '📦 Ещё одно 4':
                try:
                    with open('Groovy Script/infoForCall.groovy', 'r', encoding="utf-8") as f:
                        old_data = f.read()

                    new_data = old_data.replace('1000', '5708')

                    with open('Groovy Script/infoForCall.groovy', 'w', encoding="utf-8") as f:
                        f.write(new_data)

                    url_ACCESSKEY = f"{config.PATH}sd/services/rest/exec?accessKey={config.ACCESSKEY}"

                    files = [
                        ('script', ('infoForCall.groovy', open('Groovy Script/infoForCall.groovy', 'rb'),
                                    'application/octet-stream'))
                    ]
                    headers = config.headers

                    responseNSD = requests.request("POST", url_ACCESSKEY, headers=headers, data={}, files=files)

                    dataResponse = responseNSD.text

                    bot.send_message(message.chat.id, text=dataResponse, parse_mode="HTML")

                    new_data2 = new_data.replace('5708', '1000')
                    with open('Groovy Script/infoForCall.groovy', 'w', encoding="utf-8") as f:
                        f.write(new_data2)
                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '🔱 Другое':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🛠️ Настройка напоминаний')
                item2 = types.KeyboardButton('🗿 Стикер')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, back)

                bot.send_message(message.chat.id, '🔱 Другое', reply_markup=markup)

            elif message.text == '🌬️ Алиса':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                item1 = types.KeyboardButton(f'🔦 Торшер: 🌕/🌑')
                item2 = types.KeyboardButton(f'🌆 Ночник: 🌕/🌑')
                item3 = types.KeyboardButton(f'💡 Люстра: 🌕/🌑')
                item4 = types.KeyboardButton(f'🤖 Беляшик: 🌕/🌑')
                item5 = types.KeyboardButton(f'❓Очиститель')
                item6 = types.KeyboardButton(f'❓Телевизор')
                item7 = types.KeyboardButton(f'💫 Чиллим')
                item8 = types.KeyboardButton(f'🗻 Я ушёл')

                back = types.KeyboardButton('◀ Назад')
                markup.row(item1, item2, item3)
                markup.row(item4, item5, item6)
                markup.row(item7, item8)
                markup.row(back)

                bot.send_message(message.chat.id, '🌬️ Алиса', reply_markup=markup)

            elif message.text.__contains__('🔦 Торшер'):
                if state_dev(config.TORCH):
                    run_scen(config.ON_TORCH)
                    state_t = '🔦 Торшер: 🌑'
                else:
                    run_scen(config.OFF_TORCH)
                    state_t = '🔦 Торшер: 🌕'

                bot.send_message(message.chat.id, state_t)

            elif message.text.__contains__('🤖 Беляшик'):
                if state_dev(config.RVC):
                    run_scen(config.ON_RVC)
                    state_t = '🤖 Беляшик: 🌑'
                else:
                    run_scen(config.OFF_RVC)
                    state_t = '🤖 Беляшик: 🌕'

                bot.send_message(message.chat.id, state_t)

            elif message.text.__contains__('🌆 Ночник'):
                if state_dev(config.NIGHTLIGHT):
                    run_scen(config.ON_NIGHTLIGHT)
                    state_t = '🌆 Ночник: 🌑'
                else:
                    run_scen(config.OFF_NIGHTLIGHT)
                    state_t = '🌆 Ночник: 🌕'

                bot.send_message(message.chat.id, state_t)

            elif message.text.__contains__('💡 Люстра'):
                if state_dev(config.CHANDELIER):
                    run_scen(config.ON_CHANDELIER)
                    state_t = '💡 Люстра: 🌑'
                else:
                    run_scen(config.OFF_CHANDELIER)
                    state_t = '💡 Люстра: 🌕'

                bot.send_message(message.chat.id, state_t)

            elif message.text.__contains__('💫 Чиллим'):
                try:
                    run_scen(config.СHILL)
                    state = 'Ееее Чиллим!!! Выключаем люстру, включаем ночник!'

                    bot.send_message(message.chat.id, state)

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text.__contains__('🗻 Я ухожу'):
                try:
                    run_scen(config.IM_OUT)
                    state = 'Выключаем всё!'

                    bot.send_message(message.chat.id, state)

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

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

            elif message.text == '📍 Запуск планировщика':
                try:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item2 = types.KeyboardButton('📍 Запуск планировщика')
                    item3 = types.KeyboardButton('🗒️ Все даты')
                    back = types.KeyboardButton('◀ Назад')
                    markup.add(item2, item3, back)

                    # thread = Thread(target=run(message, markup))
                    # thread.start()

                except:
                    bot.send_message(chat_id=message.chat.id, text='Что-то пошло не по плану :(')

            elif message.text == '🗒️ Все даты':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('📍 Запуск планировщика')
                item2 = types.KeyboardButton('🗒️ Все даты')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, back)

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
                                         text=row[0] + "\nДата: " + row[2] + "-" +
                                              row[1])

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

            elif message.text == '🔮 Узнаем погоду':
                '''Переписать города под Inline-кнопки'''

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🏤 Москва')
                item2 = types.KeyboardButton('🚣 Санкт-Петербург')
                back = types.KeyboardButton('◀ Назад')
                markup.add(item1, item2, back)

                bot.send_message(message.chat.id, '🔮 Узнаем погоду', reply_markup=markup)

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

            elif message.text == '◀ Назад':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('🎇 Рандомное число')
                item2 = types.KeyboardButton('🔮 Узнаем погоду')
                # item3 = types.KeyboardButton('🍩 ITSM365')
                item4 = types.KeyboardButton('🌬️ Алиса')
                item5 = types.KeyboardButton('🔱 Другое')

                markup.row(item1, item2)
                markup.row(item4, item5)

                bot.send_message(message.chat.id, '◀ Назад', reply_markup=markup)


    else:
        bot.send_message(message.chat.id, message.text)


class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()

#Запускается так потому что два потока, сам бот и планировщик
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
