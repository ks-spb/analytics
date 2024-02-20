import math
import inspect
from datetime import datetime

from function import old_date, get_google_document, get_article_dict
from wildberries_client import WbOrder, WbSale, WbStock


MONTH = 3  # Месяцев, за которые делается отчет
DAYS_BEFORE_DELIVERY = 10  # Сколько дней до отгрузки
DAYS_LEFT = 30  # На сколько дней должно хватить поставки


class Calculator:
    """Класс для хранения всех исходных данных.
    Возвращает значение любого поля. Предварительно, если нужно, произведя его расчет
    Для каждого поля имеет отдельный метод"""

    def __init__(self):
        """Подготавливает набор исходных данных:
         - Таблица Google
         - Отчет о Заказах
         - Отчет о Продажах
         - Отчет об Остатках"""
        self.old_date = old_date(MONTH)  # Расчет даты с которой прошло указанное количество месяцев
        current_datetime = datetime.now()
        self.to_date = current_datetime.strftime("%Y-%m-%d")
        old = datetime.strptime(self.old_date, '%Y-%m-%d')
        self.days_passed = (current_datetime - old).days  # Дней прошло с выбранной даты до текущей
        print(f'Отчет за {self.days_passed} дней. С {self.old_date}')
        self.article = None  # Текущий артикул продавца (из строки которая обрабатывается)
        self.article_wb = None  # Артикул WB соответствующий артикулу продавца
        self.google_data = get_google_document()  # Получение google документа в виде словаря
        self.result = dict()  # Результаты вычислений {"имя поля": значение}
        self.line = None
        try:
            self.orders_obj = WbOrder()  # Объект заказов
            self.orders_obj.get_report(self.old_date)  # Получить заказы
            self.orders = self.orders_obj.summary()  # Получаем словарь с данными по каждому артикулу
        except Exception:
            exit('Ошибка получения заказов')
        try:
            self.sales_obj = WbSale()  # Объект продаж
            self.sales_obj.get_report(self.old_date)  # Получить продажи
            self.sales = self.sales_obj.summary()  # Получаем словарь с данными по каждому артикулу
        except Exception:
            exit('Ошибка получения продаж')
        try:
            self.stocks_obj = WbStock()  # Объект остатков
            self.stocks_obj.get_report(self.old_date)  # Получить остатки
            self.stocks = self.stocks_obj.summary()  # Получаем словарь с данными по каждому артикулу
        except Exception:
            exit('Ошибка получения остатков')

        # Получаем словарь артикулов для перевода {артикул в Google документе: артикул в WB}
        self.article_dict = get_article_dict()

    def get_next_article(self):
        """Переходит к следующей строке в списке словаря
        и возвращает артикул товара, который описан в этой строке.
        Если счетчик строк имеет значение None - начинает с первой записи.
        Если записей больше нет - возвращает None."""
        if self.line is None:
            self.line = -1
        self.line += 1
        if self.line < len(self.google_data['артикул']):
            self.article = self.google_data['артикул'][self.line]
            self.article_wb = self.get_wb_article(self.article)
            return self.article
        return None

    def get_wb_article(self, article):
        """Получение артикула WB по артикулу продавца"""
        if article not in self.article_dict:
            # Если артикула нет в справочнике, значит он такой-же
            return article
        return self.article_dict[article]

    # ---------------------------------------------------------------------------------
    # Методы получения значений полей

    # Каждый метод записывает результат своего вычисления, для текущей строки в словарь с ключом по имени метода.
    # Он может быть извлечен в дальнейшем другими методами по имени функции которая его рассчитала.

    def product_name(self):
        """Наименование продукта"""
        name = inspect.currentframe().f_code.co_name  # Название текущей функции
        self.result[name] = self.google_data['Наименование Ozon'][self.line]
        return self.result[name]

    def product_article(self):
        """Артикул продукта продавца"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = self.article
        return self.result[name]

    def product_article_wb(self):
        """Артикул продукта WB"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = self.article_wb
        return self.result[name]

    def status(self):
        """Статус"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = self.google_data['Статус'][self.line]
        return self.result[name]

    def ordered(self):
        """Сколько товаров заказано"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.article_wb in self.orders:
            self.result[name] = self.orders[self.article_wb]['quantity']
        return self.result[name]

    def ordered_sum(self):
        """Сумма заказов с комиссией WB"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.article_wb in self.orders:
            self.result[name] = self.orders[self.article_wb]['finishedPrice']
        return self.result[name]

    def purchased(self):
        """Сколько товаров выкуплено"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.article_wb in self.sales:
            self.result[name] = self.sales[self.article_wb]['quantity']
        return self.result[name]

    def purchased_sum(self):
        """Сумма покупок"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.article_wb in self.sales:
            self.result[name] = self.sales[self.article_wb]['forPay']
        return self.result[name]

    def leftover(self):
        """Остаток"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.article_wb in self.stocks:
            self.result[name] = self.stocks[self.article_wb]['quantity']
        return self.result[name]

    def price_one_item(self):
        """Стоимость 1 шт. товара"""
        name = inspect.currentframe().f_code.co_name
        if self.result['purchased']:
            self.result[name] = round(self.result['purchased_sum'] / self.result['purchased'], 2)
        else:
            self.result[name] = 0
        return self.result[name]

    def sales_days(self):
        """Количество дней продаж"""
        return self.days_passed

    def sales_speed(self):
        """Скорость продаж"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = round(self.result['purchased'] / self.days_passed, 2)
        return self.result[name]

    def days_left(self):
        """На сколько дней хватит остатков"""
        name = inspect.currentframe().f_code.co_name
        if self.result['purchased'] == 0:
            # Если продаж 0, то указываем что остатков хватит на 999 дней
            self.result[name] = 999
        if self.result['leftover'] == 0:
            # Если остаток 0, то указываем что остатков хватит на 0 дней
            self.result[name] = 0
        if self.result['sales_speed']:
            self.result[name] = int(self.result['leftover'] / self.result['sales_speed'])
        return self.result[name]

    def days_before_delivery(self):
        """Сколько дней до отгрузки"""
        return DAYS_BEFORE_DELIVERY

    def days_left_to_delivery(self):
        """На сколько дней должно хватить поставки"""
        return DAYS_LEFT

    def old_delivery(self):
        """Старый вариант поставки"""
        name = inspect.currentframe().f_code.co_name
        var = DAYS_BEFORE_DELIVERY + DAYS_LEFT
        if self.result['days_left'] <= var:
            self.result[name] = math.ceil(var * self.result['sales_speed'] - self.result['leftover'])
            if self.result[name] < 0:
                self.result[name] = 0
        return self.result[name]

    def delivery_filter(self):
        """Поставка по стоимости (фильтр)"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 0
        if self.result['old_delivery'] >= 3:
            if self.result['price_one_item'] >= 300 or self.result['old_delivery'] >= 10:
                self.result[name] = self.result['old_delivery']
        return self.result[name]


    def stub(self):
        """Заглушка"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = None
        return self.result[name]

    def code_1c(self):
        """Код 1С"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = self.google_data['Код 1С'][self.line]
        return self.result[name]

    def specification(self):
        """Спецификация"""
        name = inspect.currentframe().f_code.co_name
        self.result[name] = 'Основная'
        return self.result[name]

