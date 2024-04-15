# Работа с Wildberries
# Продажи (Статистика)

import requests
import json

# Расчеты
# data = json.loads(open('data_sales.json', 'r', encoding='utf-8').read())

# print(data)
# print(len(data))
# exit()



url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

params = {
    'dateFrom': '2024-02-25',
    'flag': 1,
}

# response = requests.post(url, headers=headers, params=params)
response = requests.get(url, headers=headers, params=params)

data = json.loads(response.content)

print(data)

# Открываем файл для записи
with open('../data_sales.json', 'w', encoding='utf-8') as file:
    # Записываем данные в файл с правильным форматированием
    json.dump(data, file, indent=4, ensure_ascii=False)

