# -*- coding:utf-8 -*-
from telebot import TeleBot
from libs.constants import TOKEN
from libs.AccuWeather import AccuWeather

bot = TeleBot(TOKEN)
apiAW = AccuWeather()

print(bot.get_me())


def log(message, answer):
    print('\n--------')

    from datetime import datetime
    print(datetime.now())
    _msg = 'Сообщение от {0} {1}. (id = {2}) \nТекст: {3}'.format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text)
    print(_msg)
    print("Ответ: "+answer)


def extract_args_from_text(text):
    text = text
    text = text.replace('/getweather', '')
    result_text_split = text.split(',')

    if len(result_text_split) > 0 and result_text_split[0].strip()!='':
        params = {'city': result_text_split[0].strip() if len(result_text_split) > 0 else '',
                  'mode': result_text_split[1].strip() if len(result_text_split) > 1 else 'daily',
                  'details_mode': result_text_split[2].strip() if len(result_text_split) > 2 else '1'}
    else:
        params = None

    return params


@bot.message_handler(commands=['getweather'])
def handle_command(message):
    params = extract_args_from_text(str(message.text))
    if params != None:
        forecast = apiAW.get_weather(params.get('city'),
                                     params.get('mode'),
                                     params.get('details_mode'))
    else:
        forecast = 'Не найдены параметры метода'

    log(message, forecast)
    bot.send_message(message.chat.id, forecast)


@bot.message_handler(commands=['getforecastingmode'])
def handle_command(message):
    modes = apiAW.get_forecasting_mode()
    log(message, modes)
    bot.send_message(message.chat.id, modes)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    pass


bot.polling(none_stop=True, interval=0)