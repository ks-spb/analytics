# Отчет использует Google документ и API Wb

import string
from openpyxl import Workbook, styles
from openpyxl.styles import PatternFill

from calculator import Calculator


calculator = Calculator()  # Создаем объект со всеми исходными данными и методами расчета полей

# Регистрация методов для рассчета полей

fields = {
    'Наименование товара': calculator.product_name,
    'Артикул продавца': calculator.product_article,
    'Артикул WB': calculator.product_article_wb,
    'Статус': calculator.status,
    'Заказано': calculator.ordered,
    'Сумма заказов с комиссией WB': calculator.ordered_sum,
    'Выкупили': calculator.purchased,
    'К перечислению': calculator.purchased_sum,
    'Остаток': calculator.leftover,
    'Стоимость 1 шт.': calculator.price_one_item,
    'Дней продаж': calculator.sales_days,
    'Скорость продаж': calculator.sales_speed,
    'Остатка хватит, дней': calculator.days_left,
    'Дней до отгрузки': calculator.days_before_delivery,
    'На сколько дней поставка': calculator.days_left_to_delivery,
    'Старый вариант поставки': calculator.old_delivery,
    'Поставка по стоимости (фильтр)': calculator.delivery_filter,
    'Код 1С': calculator.code_1c,
    'Спецификация': calculator.specification,
}

# Ширина столбцов по номерам
width_column = [80, 15, 15] + [12]*30

# Создаем новый документ
wb = Workbook()

# Получаем активный лист
ws = wb.active

# Добавляем заголовки полей в первую строку
ws.append([i for i in fields.keys()])

# Добавляем данные
while not calculator.get_next_article() is None:
    row = []
    for name_field, method in fields.items():
        try:
            row.append(method())
        except:
            pass
    ws.append(row)

# Закрепление областей
ws.freeze_panes = 'D2'

# Устанавливаем перенос по словам для ячеек в диапазоне от 1-20 первой строки
for col in range(1, 21):
    cell = ws.cell(row=1, column=col)
    cell.alignment = styles.Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width_column[col-1]

# # Применение цветов
# red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
# # ws['A1':'A5'].apply(lambda x: setattr(x, 'fill', red_fill))
# for row in ws['A1:A5']:
#     for cell in row:
#         cell.fill = red_fill


# Сохраняем документ
old = calculator.old_date.replace('-', '.')
to = calculator.to_date.replace('-', '.')
wb.save(f'Report {old} - {to}.xlsx')

