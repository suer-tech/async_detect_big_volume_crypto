from datetime import datetime
import pytz
import re
from tinkoff.invest.services import MarketDataStreamManager

from tinkoff.invest import (
    CandleInstrument,
    Client,
    SubscriptionInterval,
)
from config import tinkoff

TOKEN = tinkoff

#
# def main():
#     with Client(TOKEN) as client:
#         inst = client.instruments.find_instrument(query='Курс юань - рубль', api_trade_available_flag=True)
#         print(inst)
#         for cur in inst.instruments:
#             print(cur)
#             print('')
# main()
#

import json
import time


def subscribe_and_save_price(asset, result_prices_arr):
    print(asset)
    with Client(TOKEN) as client:
        market_data_stream: MarketDataStreamManager = client.create_market_data_stream()
        market_data_stream.candles.waiting_close().subscribe(
            [
                CandleInstrument(
                    figi=asset['code'],
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ]
        )
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts:
            for marketdata in market_data_stream:
                if marketdata.candle:
                    last_price = marketdata.candle.close

                    last_price_units = last_price.units
                    last_price_nano = last_price.nano

                    # Преобразование в число с учетом nano
                    numeric_value = float(f"{last_price_units}.{last_price_nano}")


                    if asset['code'] not in result_prices_arr:

                        print(numeric_value)
                        return numeric_value
                    else:
                        return None
            attempts += 1

        print(f"Unable to get price for {asset['code']} after {max_attempts} attempts.")
        return None


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
    if len(basket_price) >= 2:
        if currience != eur:
            # Получаем второй и третий элементы
            values = list(basket_price.values())
            first_element = values[0]
            second_element = values[1]
            third_element = values[2]

            # Извлекаем значения из элементов
            value_first = float(first_element)
            value_second = float(second_element)
            value_third = float(third_element) / x

        else:
            values = list(basket_price.values())
            second_element = values[0]
            third_element = values[1]

            # Извлекаем значения из элементов
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

def extract_i(file_path):
    values = []

    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                value = float(data['data'].split(',')[1].strip()[1:-1])
                values.append(value)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
            except (IndexError, ValueError) as e:
                print(f"Error extracting value from file {file_path}: {e}")

    return values



def get_last_value(file_path):
    try:
        with open(file_path, 'r') as file:
            # Читаем все строки из файла
            lines = file.readlines()

            # Если файл пуст, возвращаем None
            if not lines:
                return None

            # Извлекаем последнюю строку и используем регулярное выражение для поиска числа
            last_line = lines[-1]
            match = re.search(r'[-+]?\d*\.\d+', last_line)

            if match:
                value = float(match.group())
                return value
            else:
                print(f"Error extracting value from {file_path}: No valid number found.")
                return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error extracting value from {file_path}: {e}")
        return None

# Пример использования функции
usd_file_path = 'usd.txt'
last_value = get_last_value(usd_file_path)

if last_value is not None:
    print(f"Last value in {usd_file_path}: {last_value:.3f}")
else:
    print(f"Error getting last value from {usd_file_path}.")



def write_all_spread():
    usd_file_path = 'usd.txt'
    eur_file_path = 'eur.txt'
    cny_file_path = 'cny.txt'
    output_file_path = 'all_spread.txt'

    x_value = get_last_value(usd_file_path)
    y_value = get_last_value(eur_file_path)
    z_value = get_last_value(cny_file_path)

    if None in (x_value, y_value, z_value):
        print("Error extracting values from files. Check the file contents.")
        return

    with open(output_file_path, 'w') as output_file:
        output_file.write(f'USD: {x_value:.3f}\n')
        output_file.write(f'EUR: {y_value:.3f}\n')
        output_file.write(f'CNY: {z_value:.3f}\n')

    print('Data successfully written to all_spread.txt.')




# Создаем файлы под запрос пользователя о позах-----------------------------------------------------------------------------
def createTxtFile(txt_file):
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError as err:
        with open(txt_file, 'w') as fw:
            pass

usd = (

    {'code': 'BBG0013HGFT4'},  # USDRUB
    {'code': 'FUTUSDRUBF00'},
    {'code': 'FUTSI0324000'}  # SIZ3
)

eur = (


    {'code': 'FUTEURRUBF00'},
    {'code': 'FUTEU0324000'}  # SIZ3
)

cny = (

    {'code': 'BBG0013HRTL0'},  # USDRUB
    {'code': 'FUTCNYRUBF00'},
    {'code': 'FUTCNY032400'}  # SIZ3
)


while True:

    try:

        try:
            f = open('sig_proc.txt', 'r')
        except FileNotFoundError as err:
            with open('sig_proc.txt', 'w') as fw:
                pass

        # Создайте словарь для сохранения цен активов
        usd_prices = {}
        eur_prices = {}
        cny_prices = {}

        # Подпишитесь на стакан для каждого актива
        for asset in usd:
            if asset['code'] not in usd:
                price = subscribe_and_save_price(asset, usd_prices)
                if price != None:
                    usd_prices[asset['code']] = price
        print(usd_prices)

        # В asset_prices будут сохранены цены активов
        diff = calculate_difference(usd, usd_prices)
        if diff is not None:
            write_spread(usd, diff)


        # Подпишитесь на стакан для каждого актива
        for asset in eur:
            if asset['code'] not in eur:
                price = subscribe_and_save_price(asset, eur_prices)
                if price != None:
                    eur_prices[asset['code']] = price
        print(eur_prices)

        # В asset_prices будут сохранены цены активов
        diff = calculate_difference(eur, eur_prices)
        if diff is not None:
            write_spread(eur, diff)


        # Подпишитесь на стакан для каждого актива
        for asset in cny:
            if asset['code'] not in cny:
                price = subscribe_and_save_price(asset, cny_prices)
                if price != None:
                    cny_prices[asset['code']] = price
        print(cny_prices)

        # В asset_prices будут сохранены цены активов
        diff = calculate_difference(cny, cny_prices)
        if diff is not None:
            write_spread(cny, diff)

        # Запись всех спредов в один файл
        write_all_spread()


    except Exception as e:
        print("Возникла непредвиденная ошибка.")
        time.sleep(5)

    time.sleep(900)
