import json
import requests

from decimal import *
from collections import defaultdict


class CurrencyException(Exception):
    pass


class DefUser:
    def __init__(self):
        self.f = "RUB"
        self.t = "USD"


class UserDB:
    def __init__(self):
        self.db = defaultdict(DefUser)

    def change_from(self, user_id, val):
        self.db[user_id].f = val

    def change_to(self, user_id, val):
        self.db[user_id].t = val

    def get_pair(self, user_id):
        user = self.db[user_id]
        return user.f, user.t


class Convertor:
    @staticmethod
    def get_price(values):
        vals1, vals2, summ = values
        if vals1 == vals2:
            raise CurrencyException(f'Невозможно перевести одинаковые валюты {vals2}')
        try:
            summ = float(summ.replace(',', '.'))
        except ValueError:
            raise CurrencyException(f'Не удалось обработать значение - {summ}')
        if summ <= 0:
            raise CurrencyException(f'Сумма должна быть больше 0.')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={vals1}&tsyms={vals2}')
        result = Decimal((json.loads(r.content)[vals2]) * summ)
        return round(result, 2)

        # if db[0] == vals[1][1]:
        #     raise CurrencyException(f'Невозможно перевести одинаковые валюты {vals[1][1]}')
        # try:
        #     values = float(values)
        # except ValueError:
        #     raise CurrencyException(f'Не удалось обработать значение - {values}')
        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={vals[1][0]}&tsyms={vals[1][1]}')
        # print(json.loads(r.content))
        # result = Decimal((json.loads(r.content)[vals[1][1]]) * values)
        # return round(result, 2)
