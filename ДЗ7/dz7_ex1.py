# Задание 1. Получение данных из публичного API
import requests

n = 5
response = requests.get('https://jsonplaceholder.typicode.com/posts/')
if response.status_code == 200:
    data = response.json()[0:n]
    for i in range(n):
        print(f'Пост № {i+1}\nЗаголовок:')
        print(data[i]['title'])
        print('Тело:')
        print(data[i]['body'])
else:
    print(f'Ошибка: {response.status_code}')
