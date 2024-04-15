# Работа с Wildberries

import requests
import json

url = "https://suppliers-api.wb.ru/content/v1/analytics/nm-report/detail"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

params = {
    'period': {
        'begin': '2023-10-11 00:00:00',
        'end': '2024-01-11 00:00:00',
    },
    'page': 0,
}

params = {
  "brandNames": [],
  "objectIDs": [],
  "tagIDs": [],
  "nmIDs": [],
  "timezone": "Europe/Moscow",
  "period": {
    "begin": "2023-10-11 20:05:32",
    "end": "2024-01-11 20:05:32"
  },
  "page": 1
}
# response = requests.post(url, headers=headers, params=params)
response = requests.post(url, headers=headers, data=json.dumps(params))

data = json.loads(response.content)

print(response.status_code)
# Открываем файл для записи
with open('data.json', 'w') as file:
    # Записываем данные в файл с правильным форматированием
    json.dump(data, file, indent=4)
