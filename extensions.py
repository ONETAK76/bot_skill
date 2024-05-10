import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = CurrencyConverter.get_currency_key(base)
            quote_key = CurrencyConverter.get_currency_key(quote)
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_key}')
            rates = response.json()['rates']
            base_to_quote_rate = rates[quote_key]
            return base_to_quote_rate * amount
        except Exception as e:
            raise APIException(f'Ошибка при конвертации валюты: {e}')

    @staticmethod
    def get_currency_key(currency_name):
        currency_keys = {
            'доллар': 'USD',
            'евро': 'EUR',
            'рубль': 'RUB'
        }
        try:
            return currency_keys[currency_name.lower()]
        except KeyError:
            raise APIException(f'Валюта {currency_name} не поддерживается.')

