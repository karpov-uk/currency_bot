import requests
import json
from config import API_KEY, currency


class ExchangeException(Exception):
    pass

class ExchangeHandler:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # если указаны одинаковые валюты
        if quote == base:
            raise ExchangeException(f'Невозможно перевести одинаковые валюты: {base}')

        # обрабатываем ошибку ввода валюты
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ExchangeException(f'Неверно введена валюта {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ExchangeException(f'Неверно введена валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'Неверно указано количество "{amount}"')

        # отправляем запрос
        r = requests.get(
            f'http://api.exchangeratesapi.io/v1/latest'
            f'?access_key={API_KEY}'
            f'&base={quote_ticker}'
            f'&symbols={base_ticker}'
            )

        total_base = json.loads(r.content)['rates'][base_ticker]
        return total_base