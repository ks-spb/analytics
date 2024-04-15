# Работа с Wildberries
# Заказы (Отчет о продажах по реализации)

import requests
import json

# Расчеты
# data = json.loads(open('data_sales.json', 'r', encoding='utf-8').read())

# print(data)
# print(len(data))
# exit()



url = "https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

params = {
    'dateFrom': '2023-11-06T00:00:00',
    'dateTo': '2024-02-06T23:59:59',
    'rrdid': 0,
}

report = []
while True:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception('Ошибка запроса')
    data = json.loads(response.content)
    if data is None:
        break
    params['rrdid'] = data[-1]['rrd_id']
    report.extend(data)

sale = 0
for i in report:
    if i['supplier_oper_name'] == "Продажа":
        sale += 1


print(len(report))
print('Документ Продажа:', sale)

# Открываем файл для записи
with open('data_reportDetailByPeriod.json', 'w', encoding='utf-8') as file:
    # Записываем данные в файл с правильным форматированием
    json.dump(report, file, indent=4, ensure_ascii=False)

