# Получение списка поставок
# Выводится длинный список словарей. Новые идут в конце (они отсортированы)
# Не выполненные, те, что нас интересуют имеют свойство "done": false
# достаточно перебирая с конца отобрать такие, а встретив "done": true - прекратить.

import requests
import json
import base64

url = "https://suppliers-api.wildberries.ru/api/v3/supplies"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMjI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcyNDE3OTE5NCwiaWQiOiI3ZDNlYWVkOC1mNTlhLTQ1ZjktODJiMy1mNDg3ODVkNThmOTEiLCJpaWQiOjI0MjcxMzkyLCJvaWQiOjc0MzIwLCJzIjo2MCwic2lkIjoiNTQyMTI0YTktYjhlNS01ODk5LWEzODktZTk5NTNlM2IyM2IxIiwidCI6ZmFsc2UsInVpZCI6MjQyNzEzOTJ9.jjFEnkurbUTM3rJ-MmKYOanMPuLcFomkqo_MKTDrifeWBUJab6xV2I-rp4tWLD9lmfnQ4SBeYgEznKDVhdBKlA",
}

params = {
    'limit': 1000,
    'next': 0,
}

response = requests.get(url, headers=headers, params=params)
print(response.status_code, response.content)
data = json.loads(response.content)
print(data)

# formatted_data = json.dumps(data, indent=4)  # Преобразуем данные в форматированную строку JSON с отступами
#
# print(formatted_data)  # Распечатываем данные с форматированием

# Открываем файл для записи
with open('data_supplines.json', 'w', encoding='utf-8') as file:
    # Записываем данные в файл с правильным форматированием
    json.dump(data, file, indent=4, ensure_ascii=False)


# Поиск поставок находящихся на сборке
supplyIds = []
for suppline in reversed(data['supplies']):
    if not suppline['done']:
        print(json.dumps(suppline, indent=4, ensure_ascii=False))
        supplyIds.append(suppline['id'])

for id in reversed(supplyIds):

    url = f"https://suppliers-api.wildberries.ru/api/v3/supplies/{id}/orders"

    response = requests.get(url, headers=headers)
    # print(response.status_code, response.content)
    data = json.loads(response.content)
    # print(data)

    # Открываем файл для записи
    with open(f'data_supplines_{id}.json', 'w', encoding='utf-8') as file:
        # Записываем данные в файл с правильным форматированием
        json.dump(data, file, indent=4, ensure_ascii=False)


    # Получен список Сборочных заданий (это товар, может быть в разном количестве).
    # Они должны быть отсортированы по складам, а внутри по артикулам (одинаковые рядом)
    # Из всех данных нас интересуют Номер задания и Артикул (для печати этикеток)

    # Создаем списки кортежей (Номер задания, артикул) в словаре складов
    whs = dict()
    for order in data['orders']:
        whs_id = order['warehouseId']
        if whs_id in whs:
            whs[whs_id].append((order['id'], order['article']))
        else:
            whs[whs_id] = [(order['id'], order['article'])]

    # Сортируем списки кортежей по артикулам (второй элемент в кортеже)
    for tpl in whs.values():
        tpl.sort(key=lambda x: x[1])

    for i in whs.items():
        print(i)

    # Получение этикеток сборочных заданий
    url = f"https://suppliers-api.wildberries.ru/api/v3/orders/stickers"

    # Перебираем склады и кортежи в них
    for whs_number, lists in whs.items():
        to_params = []
        for tpl in lists:
            to_params.append(tpl[0])

        params = {
                "orders": to_params,
        }

        params2 = {
            'type': 'png',
            'width': 40,
            'height': 30,
        }
        response = requests.post(url, headers=headers, data=json.dumps(params), params=params2)
        # print(response.status_code, response.content)
        data = json.loads(response.content)
        # print(json.dumps(data, indent=4, ensure_ascii=False))

        # Открываем файл для записи
        with open(f'data_supplines_{whs_number}.json', 'w', encoding='utf-8') as file:
            # Записываем данные в файл с правильным форматированием
            json.dump(data, file, indent=4, ensure_ascii=False)

        # Сохранение файлов изображений
        for sticker in data['stickers']:

            # Декодирование base64 строки в бинарные данные
            decoded_data = base64.b64decode(sticker['file'])

            # Сохранение бинарных данных в файл формата png
            with open(f"img_{sticker['partA']}_{sticker['partB']}.png", "wb") as file:
                file.write(decoded_data)
