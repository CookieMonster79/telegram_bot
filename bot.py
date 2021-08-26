import telebot

import config

bot = telebot.TeleBot(config.TOKEN)

#Для тестирования
#@bot.message_handler(content_types=['text'])
#def lalala(message):
#    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.chat.id,
                     'Приветствую! Я могу показать курс обмена валют.\n' +
                     'Чтобы узнать курс, нажмите /exchange.\n' +
                     'Чтобы получить помощь, нажмите /help.'
                     )


bot.polling(none_stop=True)
