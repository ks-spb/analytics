# Работа с Wildberries

import requests
import json

url = "https://suppliers-api.wildberries.ru/api/v3/warehouses"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

# response = requests.post(url, headers=headers, params=params)
response = requests.get(url, headers=headers)
print(response.status_code, response.content)
data = json.loads(response.content)
print(data)
# Ответ:
# [{'name': 'Боровая 51', 'officeId': 225, 'id': 35196, 'cargoType': 1, 'deliveryType': 1}]

who_id = data[0]['id']
params = {
  "skus": [
    '2001585828056'
  ]
}

data = json.dumps(params)
url = f"https://suppliers-api.wildberries.ru/api/v3/stocks/{who_id}"

response = requests.post(url=url, headers=headers, data=data)
print(response.status_code, response.content)
data = json.loads(response.content)
print(data)

# {'stocks': [{'sku': '2000524742934', 'amount': 0}]}


# Открываем файл для записи
# with open('data.json', 'w') as file:
#     # Записываем данные в файл с правильным форматированием
#     json.dump(data, file, indent=4)
