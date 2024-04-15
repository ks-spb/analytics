# Работа с Wildberries
# Заказы (Статистика)

import requests
import json

url = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

params = {
    'dateFrom': '2023-11-06',
    'flag': 0,
}

# response = requests.post(url, headers=headers, params=params)
response = requests.get(url, headers=headers, params=params)

data = json.loads(response.content)

print(data)
# for i in response.text:
#     print(i)



# Открываем файл для записи
with open('data_orders.json', 'w', encoding='utf-8') as file:
    # Записываем данные в файл с правильным форматированием
    json.dump(data, file, indent=4, ensure_ascii=False)


