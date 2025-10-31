# Задание 3. Создание и обработка POST-запросов
import requests

data = {
    'title': 'название',
    'body': 'текст',
    'userId': 1
}
url = 'https://jsonplaceholder.typicode.com/posts/'
response = requests.post(url=url, data=data)
if response.status_code == 201:
    post = response.json()
    print(f"ID поста: {post['id']}")
    print(f"Содержимое поста: {post['body']}")
else:
    print(f'Ошибка: {response.status_code}')
