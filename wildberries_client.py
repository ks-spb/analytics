# Классы для работы с Wildberries и обработки получаемых с него данных

import json
import requests

from function import TOKEN_WB


class WbClient:
    """Базовый класс для классов разных запросов"""
    def __init__(self, report):
        # http заголовок
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"{TOKEN_WB}",
        }
        self.url = f"https://statistics-api.wildberries.ru/api/v1/supplier/{report}"
        self.report = None
        self.method = report

    def get_report(self, date_from, flag=None):
        """Совершает запрос к API WB
        принимает дату от которой делать отчет и если любое значение flag
        то отчет будет только за указанную дату
        Результаты помещает в виде словаря в свойство.
        Возвращает количество записей в отчете.
        """
        params = {'dateFrom': date_from}
        if flag:
            params.update({'flag': 1})

        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception('Не удалось получить статистику Wildberries. Попробуйте позже.')
        self.report = json.loads(response.content)

        with open(f'{self.method}_data.json', 'w', encoding='utf-8') as file:
            # Записываем данные в файл с правильным форматированием
            json.dump(self.report, file, indent=4, ensure_ascii=False)

        return len(self.report)

class WbOrder(WbClient):
    """Класс для получения и обработки заказов"""
    def __init__(self):
        super().__init__('orders')

    def summary(self):
        """Считает для каждого артикула:
         - количество заказов,
         - сумму поля finishedPrice.
        Возвращает словарь {'артикул': {'quantity': количество, 'SumFinishedPrice': сумма}}"""
        data = dict()
        for subject in self.report:
            if subject['incomeID'] == '':
                continue  # Не должно быть пустым поле Номер поставки
            if subject['supplierArticle'] not in data:
                data[subject['supplierArticle']] = {'quantity': 0, 'finishedPrice': 0}
            data[subject['supplierArticle']]['quantity'] += 1
            data[subject['supplierArticle']]['finishedPrice'] += float(subject['finishedPrice'])
        return data


class WbSale(WbClient):
    """Класс для получения и обработки продаж"""
    def __init__(self):
        super().__init__('sales')

    def summary(self):
        """Считает для каждого артикула:
         - количество покупок,
         - сумму поля priceWithDisc.
        Возвращает словарь {артикул: {'quantity': количество, 'priceWithDisc': сумма}}"""
        data = dict()
        for subject in self.report:
            if int(subject['finishedPrice']) <= 0:
                continue  # Не должна быть отрицательной цена
            if subject['supplierArticle'] not in data:
                data[subject['supplierArticle']] = {'quantity': 0, 'priceWithDisc': 0}
            data[subject['supplierArticle']]['quantity'] += 1
            data[subject['supplierArticle']]['priceWithDisc'] += float(subject['priceWithDisc'])
        return data


class WbStock(WbClient):
    """Класс для получения и обработки остатков складов"""

    def __init__(self):
        super().__init__('stocks')

    def summary(self):
        """Считает для каждого артикула:
         - количество остатков.
        Возвращает словарь {'артикул': {'quantity': количество}}"""
        data = dict()
        for subject in self.report:
            if subject['supplierArticle'] not in data:
                data[subject['supplierArticle']] = {'quantity': 0}
            data[subject['supplierArticle']]['quantity'] += int(subject['quantity'])
        return data
