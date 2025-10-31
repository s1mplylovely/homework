# Задание 4. Обработка ошибок и работа с данными
import requests


class CodeError(Exception):
    pass


def test_code(code: int):
    if code != 201:
        raise CodeError(f'Ошибка {code}')


data = {
    'title': 'название',
    'body': 'текст',
    'userId': 1
}
url = 'https://jsonplaceholder.typicode.com/posts/'
try:
    response = requests.post(url=url, data=data)
    test_code(response.status_code)
    post = response.json()
    print(f"ID поста: {post['id']}")
    print(f"Содержимое поста: {post['body']}")
except CodeError as e:
    print(e)
