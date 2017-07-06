# -*- coding: utf-8 -*-

import requests
import libs.constants as constants
import libs.parser_response as parser_response


class AccuWeather:
    """
    Позволяет быстро получать сведения о погоде и её изменениях с помощью
    API AccuWeather по средствам HTTP запросов.
    """

    def __init__(self):
        self.api_key = constants.API_KEY
        self.api_url = constants.API_URL
        self.login = constants.LOGIN
        self._passw = constants._PASSW

    def define_char_language(self, text):
        language = 'ru'
        en_ch = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        if text[:1] in en_ch:
            language = 'en'

        return language

    def city_search(self, text='', details=False):
        """
        Returns information for an array of locations that match the search text.
        """
        language = self.define_char_language(text)
        full_url = '{0}{1}'.format(self.api_url, '/locations/v1/cities/search')
        _params = {'apikey': self.api_key,
                   'q': text,
                   'details': details,
                   'language': language}
        try:
            r = requests.get(full_url, params=_params)
        except Exception as e:
            raise e

        if r.status_code == requests.codes.ok:
            try:
                response = r.json()
            except ValueError as e:
                response = e
        else:
            response = r.text

        return response

    def get_forecasting_mode(self):
        return 'Режимы прогноза:\n' + str({'hourly': 'Возвращает данные прогноза на следующие (1, 12, 24, 72) час(а) '
                                                     'для определенного местоположения',
                                           'daily': 'Возвращает данные прогноза на следующие (1, 5, 10) дней'})

    def get_url_for_mode(self, mode, details):
        """
        Returns the full reference to the web service method
        :param mode: 
        :param details: 
        :return: url
        """
        dict_key_mode = '%s_%s' % (mode, details)
        url = constants.DICT_MODE_URL.get(dict_key_mode)
        return url

    def get_weather_for_mode(self, url, location_key, details='true', language='ru'):
        _params = {'apikey': self.api_key,
                   'details': details,
                   'language': language}

        try:
            r = requests.get(url, params=_params)
        except Exception as e:
            raise e

        if r.status_code == requests.codes.ok:
            try:
                response = r.json()
            except ValueError as e:
                response = e
        else:
            response = r.text

        return response

    def get_weather(self, city, mode, details_mode):
        """
        Returns weather data for the specified city
        """

        response = self.city_search(city)

        if type([]) != type(response) or len(response) == 0:
            return 'Не удалось получить сведения по указанному городу'

        location_key = response[0].get('Key')

        if location_key == None:
            return 'Не удалось получить location_key для города %s' % city

        url = self.get_url_for_mode(mode, details_mode)
        if url == None:
            return 'Данный режим прогноза не поддерживается'
        else:
            url = '%s/%s/%s' % (self.api_url, url, location_key)

        response = self.get_weather_for_mode(url, location_key)
        if type([]) != type(response) and type({}) != type(response):
            return response

        weather = parser_response.parse(response, mode)

        return weather