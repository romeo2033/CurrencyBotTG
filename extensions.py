from config import currencies, API_key
import requests
import json

# Класс ошибок при проблеме с конвертацией
class APIException(Exception):
    pass

# Класс со статическим методом для отправки запросов к API
class Convert:
    @staticmethod
    def get_price(base, quote, amount):
        if quote == base: # Проверка, если введены одинаковые валюты
            raise APIException(f'Введены одинаковые валюты {base}')
        try:
            base_ticker = currencies[base] # Проверка, существует ли валюта
        except KeyError:
            raise APIException(f'Не смог обработать валюту "{base}"')
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не смог обработать валюту "{quote}"')
        try:
            amount = float(amount) # Проверка, верное ли число введено пользователем
        except ValueError:
            raise APIException(f'Не смог обработать кол-во: "{amount}"')

        try:
            # Отправка запроса на сервер
            conversion = requests.get(f'https://v6.exchangerate-api.com/v6/{API_key}/pair/{base_ticker}/{quote_ticker}/{amount}')
        except Exception:
            # В случае ошибки, связанной с сервером
            raise APIException('Произошла ошибка на сервере, попробуйте позднее')
        else:
            # Из ответа сервера, берем только результат конвертации и возвращаем
            conversion_result = json.loads(conversion.content)['conversion_result']
            return conversion_result

