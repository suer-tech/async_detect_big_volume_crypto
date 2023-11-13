import json
import time
import emoji
from FinamPy import FinamPy
from FinamPy.Config import Config
from datetime import datetime
import pytz
import re

MAX_ATTEMPTS = 10
WAIT_INTERVAL_SECONDS = 2

def subscribe_and_save_price(asset, result_prices_arr):
    fp_provider = FinamPy(Config.AccessToken)
    print(asset)

    def on_order_book(order_book):
        if asset['code'] not in result_prices_arr:
            result_prices_arr[asset['code']] = order_book.asks[0].price

    fp_provider.on_order_book = on_order_book
    fp_provider.subscribe_order_book(asset['code'], asset['board'], 'orderbook1')

    # Добавьте цикл ожидания с ограничением по попыткам
    attempts = 0
    while asset['code'] not in result_prices_arr and attempts < MAX_ATTEMPTS:
        time.sleep(WAIT_INTERVAL_SECONDS)
        attempts += 1

    if asset['code'] not in result_prices_arr:
        print(f"Котировки для {asset['code']} не пришли после {MAX_ATTEMPTS} попыток.")
        return False

    fp_provider.unsubscribe_order_book('orderbook1', asset['code'], asset['board'])
    fp_provider.close_channel()

def calculate_difference(currience, basket_price):

    now_utc = datetime.now(pytz.utc)

    # Преобразование времени в московское время
    moscow_timezone = pytz.timezone("Europe/Moscow")
    moscow_time = now_utc.astimezone(moscow_timezone)

    # Удаление секунд и микросекунд
    moscow_time = moscow_time.replace(second=0, microsecond=0)

    if currience == usd:
        quarterly = 'Si'
        perpetual = 'USDRUBF'
        x = 1000

    if currience == eur:
        quarterly = 'Eu'
        perpetual = 'EURRUBF'
        x = 1000

    if currience == cny:
        quarterly = 'Cny'
        perpetual = 'CNYRUBF'
        x = 1

    # Проверка, что в списке есть как минимум три элемента
    if len(basket_price) >= 3:
        # Получаем второй и третий элементы
        values = list(basket_price.values())
        first_element = values[0]
        second_element = values[1]
        third_element = values[2]

        # Извлекаем значения из элементов
        value_first = float(first_element)
        value_second = float(second_element)
        value_third = float(third_element) / x

        # Вычисляем разницу
        difference = "{:.3f}".format(value_third - value_second)
        result = f"[{moscow_time}, {difference}]"

        print(result)

        return result

def write_spread(currience, diff):
    txt = 'usd.txt'
    if currience == eur:
        txt = 'eur.txt'
    if currience == cny:
        txt = 'cny.txt'

    with open(txt, 'a', encoding='utf-8') as file:
        spread_obj = {"data": diff}
        spread_str = json.dumps(spread_obj, ensure_ascii=False)  # Преобразование в строку JSON
        file.write(spread_str + '\n')  # Запись строки в файл с добавлением новой строки


def write_connection_error(currience, diff):
    txt = 'usd.txt'
    if currience == eur:
        txt = 'eur.txt'
    if currience == cny:
        txt = 'cny.txt'

    with open(txt, 'w', encoding='utf-8') as file:
        pass
        file.write(diff)

def write_all_spread():
    currencies = ['USD', 'EUR', 'CNY']

    with open('all_spread.txt', 'w', encoding='utf-8') as all_file:
        for currency in currencies:
            file_name = f'{currency}.txt'
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                if lines:
                    last_line = json.loads(lines[-1])
                    print(last_line)
                    spread_value = re.search(r'\d+\.\d+', last_line['data']).group()
                    spread_str = f"{currency.upper()}: {float(spread_value):.3f}\n"
                    all_file.write(spread_str)


# Создаем файлы под запрос пользователя о позах-----------------------------------------------------------------------------
def createTxtFile(txt_file):
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError as err:
        with open(txt_file, 'w') as fw:
            pass

usd = (

    {'board': 'CETS', 'code': 'USD000UTSTOM'},  # USDRUB
    {'board': 'FUT', 'code': 'USDRUBF'},
    {'board': 'FUT', 'code': 'SiZ3'}  # SIZ3
)

eur = (

    {'board': 'CETS', 'code': 'EUR_RUB__TOM'},  # USDRUB
    {'board': 'FUT', 'code': 'EURRUBF'},
    {'board': 'FUT', 'code': 'EuZ3'}  # SIZ3
)

cny = (

    {'board': 'CETS', 'code': 'CNYRUB_TOM'},  # USDRUB
    {'board': 'FUT', 'code': 'CNYRUBF'},
    {'board': 'FUT', 'code': 'CRZ3'}  # SIZ3
)


while True:

    createTxtFile('usd.txt')
    createTxtFile('eur.txt')
    createTxtFile('cny.txt')
    createTxtFile('all_spread.txt')

    spread_arr = []

    # Создайте словарь для сохранения цен активов
    usd_prices = {}
    eur_prices = {}
    cny_prices = {}

    # Подпишитесь на стакан для каждого актива
    for asset in usd:
        subscribe_and_save_price(asset, usd_prices)
        if not subscribe_and_save_price(asset, usd_prices):
            write_connection_error(usd, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(usd_prices)
    diff = calculate_difference(usd, usd_prices)
    if diff is not None:
        write_spread(usd, diff)


    # Подпишитесь на стакан для каждого актива
    for asset in eur:
        subscribe_and_save_price(asset, eur_prices)
        if not subscribe_and_save_price(asset, eur_prices):
            write_connection_error(eur, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(eur_prices)
    diff = calculate_difference(eur, eur_prices)
    if diff is not None:
        write_spread(eur, diff)


    # Подпишитесь на стакан для каждого актива
    for asset in cny:
        subscribe_and_save_price(asset, cny_prices)
        if not subscribe_and_save_price(asset, cny_prices):
            write_connection_error(cny, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(cny_prices)
    diff = calculate_difference(cny, cny_prices)
    if diff is not None:
        write_spread(cny, diff)

    # Запись всех спредов в один файл
    write_all_spread()


    time.sleep(2)

