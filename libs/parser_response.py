# -*- coding: utf-8 -*-


def convert_to_celsius(f):
    c = int((int(f) - 32) * (5/9))
    return str(c)


def convert_to_ms(mi_h):
    ms = int(mi_h) * 0.44704
    return '%.2f' %ms


def parse(response, mode):
    if str(mode).lower() == 'hourly':
        return parse_response_hourly(response)
    else:
        return parse_response_daily(response)


def parse_response_hourly(response):
    return 'Данный режим прогноза на текущий момент не поддерживается'


def parse_response_daily(response):
    root = response.get('DailyForecasts')
    headline = response.get('Headline')
    sb = []
    for DailyForecast in root:
        date = DailyForecast.get('Date')
        min_temperature = DailyForecast.get('Temperature').get('Minimum')
        max_temperature = DailyForecast.get('Temperature').get('Maximum')
        Day = DailyForecast.get('Day')
        Night = DailyForecast.get('Night')

        sb.append('-------------------\nПрогноз на %s\n'
                  'Днем: до %s`C, %s, ветер %s м/с\n'
                  'Ночью: от %s`C, %s, ветер %s м/с\n'
                  '-------------------'
                  % (date[:10],
                     convert_to_celsius(max_temperature['Value']) if max_temperature['Unit'] == 'F' else max_temperature['Value'],
                     Day.get('LongPhrase'),
                     convert_to_ms(Day['WindGust']['Speed']['Value']),
                     convert_to_celsius(min_temperature['Value']) if min_temperature['Unit'] == 'F' else min_temperature['Value'],
                     Night.get('LongPhrase'),
                     convert_to_ms(Night['WindGust']['Speed']['Value'])))

    return ''.join(sb) + '\nБолее подробный прогноз можно узнать по ссылке: %s' % headline['Link']
