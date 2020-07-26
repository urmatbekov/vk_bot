import telebot

import config

bot = telebot.TeleBot(config.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text'])
def echo_all(message):
    answer = config.get_weather(str(message.text))
    bot.reply_to(message, answer)


bot.polling()
