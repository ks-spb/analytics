# Классы для работы с "Data collection and analysis" и обработки получаемых данных

import json
import requests

from function import TOKEN_DCA


class DCAClient:
    """Класс для разных запросов"""
    def __init__(self):
        # http заголовок
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {TOKEN_DCA}",
        }
        self.url = f"http://3f15443cefad.vps.myjino.ru/collection/v1/stocks/was-in-stock/"

    def get_fbo(self, from_date, to_date):
        """Получение данных о количестве дней в которые товары находились на складах
         FBO за указанный период.
         Принимает даты начала и конца периода.
         Возвращает словарь {артикул продавца: количество дней, ...}. Для всех товаров."""
        params = {'from_date': from_date, 'to_date': to_date}
        url = self.url + 'fbo'

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения остатков на складах FBO. {response.content}')
        return json.loads(response.content)

    def get_fbs(self, from_date, to_date):
        """Получение данных о количестве дней в которые товары находились на складах
         FBS за указанный период.
         Принимает даты начала и конца периода.
         Возвращает словарь {артикул продавца: количество дней, ...}. Для всех товаров."""
        params = {'from_date': from_date, 'to_date': to_date}
        url = self.url + 'fbs'

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения остатков на складах FBS. {response.content}')
        return json.loads(response.content)

