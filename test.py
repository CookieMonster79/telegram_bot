import telegram
from telegram.ext import Updater, CommandHandler

import config

bot = telegram.Bot(token=config.TOKEN)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Привет, мы начинаем отсчет!")

    context.job_queue.run_repeating(callback_day,
                                    interval=30,  # В секундах
                                    first=0,  # Если 0 то первое отправляется сразу
                                    context=update.message.chat_id)


def callback_day(context):
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id,
                             text="Это очередное сообщение, проверь сколько прошло времени")


def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler()
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
