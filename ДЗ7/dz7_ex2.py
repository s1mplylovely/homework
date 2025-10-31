# Задание 2. Работа с параметрами запроса
import requests

city = input('City: ')
api_key = 'e5e9eaa3cee4c90db2abf394bdcd8d8b'
limit = 1
response = requests.get(
    f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}')
if response.status_code == 200:
    lat = response.json()[0]['lat']
    lon = response.json()[0]['lon']
else:
    print(f'Ошибка Geocoding API: {response.status_code}')

response = requests.get(
    f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')

if response.status_code == 200:
    data = response.json()
    weather, temp = data['weather'][0]['description'], data['main']['temp']
    print(f'Current weather:\n{weather}, {round(temp-273, 1)} C')
else:
    print(f'Ошибка Current weather API: {response.status_code}')
