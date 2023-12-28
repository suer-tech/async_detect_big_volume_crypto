import datetime
import json
import os
import time
import binance
import emoji
import requests
import time
from statistics import median

import threading
from unicodedata import decimal

limit = 500
median_x = 3
buy_sell_ratio_x = 7


# Переводим время в удобочитаемый вид-----------------------------------------------------------------------------
def convert_time(timestamp):
    timestamp_seconds = timestamp / 1000
    dt = datetime.datetime.fromtimestamp(timestamp_seconds, tz=datetime.timezone.utc)
    return (dt.strftime("%Y-%m-%d %H:%M:%S %Z"))


# Запрос обьемов с биржи-----------------------------------------------------------------------------
def get_buy_sell_ratio(symbol, interval, limit=500):
    url = "https://fapi.binance.com/futures/data/takerlongshortRatio"
    params = {
        "symbol": symbol,
        "period": interval,
        "limit": limit,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None


# Запрос свечек с биржи-----------------------------------------------------------------------------
def get_kline_data(symbol, interval, limit=500, startTime=None, endTime=None):
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": startTime,
        "endTime": endTime
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None


# Считаем высоту свечи в %-----------------------------------------------------------------------------
def check_diff_percent(data):
    result = [
        {k[0]: round((float(k[2]) - float(k[3])) / float(k[2]) * 100, 4)}
        for k in data
    ]

    return result


# Считаем среднюю высоту свечи в % за период limit-----------------------------------------------------------------------------
def calculate_median(data_list):
    values = [float(list(item.values())[0]) for item in data_list]
    return median(values)


# Считаем средний объем за период limit отсеиваем небольшие объемы-----------------------------------------------------------------------------
def calculate_average_vol(data, volume):
    diff = buy_sell_ratio_x

    averg_vol = sum([float(vol[5]) for vol in data])/limit

    if float(volume) > averg_vol * diff:
        return volume


# Создаем файлы под запрос пользователя о позах-----------------------------------------------------------------------------
def createTxtFile(txt_file):
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError as err:
        with open(txt_file, 'w') as fw:
            pass


def get_symbolPrice_ticker():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None


def run_process(sym):
    try:
        data = get_kline_data(sym, '1h', limit=500) # получаем данные всех свечек за период
        data_last = data[-2] # получаем данные последней свечки за период
        volume = data_last[5]  # получаем данные по обьемам последней закрытой свечки за период
        checked_last = calculate_average_vol(data, volume) # сравниваем обьем на последней свечке и если он больше среднеиго то возвращаем эту свечку

        if checked_last:
            diff_procent = check_diff_percent(data)  # считаем высоту всех свечек за период
            diff_procent_last = diff_procent[-2]  # получаем высоту последней свечки за период
            value_last = next(iter(diff_procent_last.values()))  # получаем высоту последней свечки за период
            mediana = calculate_median(diff_procent)  # считаем среднюю высоту свечки за период

            if mediana * median_x > float(value_last):
                this_time = datetime.datetime.now()  # Получаем текущее время
                time_signal = datetime.datetime.strptime(convert_time(int(data_last[0])), "%Y-%m-%d %H:%M:%S %Z")

                t_vol = this_time - time_signal

                # Сигнал большого обьема----------------------------
                if t_vol.total_seconds() <= 45000:  # 900 секунд = 15 минут

                    for symb in symb_index:
                        if symb['symbol'] == sym:
                            price = float(symb['price'])

                            long = {
                                '1 tvh': price,
                                '2 tvh': price - price / 100 * 2,
                                '3 tvh': price - price / 100 * 4,
                                'stop': price - price / 100 * 5.5,
                                'take': price + price / 100 * 2,
                            }

                            short = {
                                '1 tvh': price,
                                '2 tvh': price + price / 100 * 2,
                                '3 tvh': price + price / 100 * 4,
                                'stop': price + price / 100 * 5.5,
                                'take': price - price / 100 * 2,
                            }

                    with open('signal_vol.txt', 'w', encoding='utf-8') as fw:
                        mess = f"{emoji.emojize(':antenna_bars:Скачок объема торгов')}\n{emoji.emojize(':check_mark_button:')}{sym}\n"
                        fw.write(mess)
                        fw.write(f"\nLong\n")

                        for key, value in long.items():
                            fw.write(f"{key}: {value}\n")

                        fw.write(f"\nShort\n")
                        for key, value in short.items():
                            fw.write(f"{key}: {value}\n")
                    print(sym)
                    # Устанавливаем флаг как метку времени текущего актива
                    signal_recorded[sym] = time.time()
    except ZeroDivisionError as err:
        print('ZeroDivisionError')
        return None
    except IndexError as err:
        print('IndexError ')
        return None


# Функция для удаления устаревших записей
def clean_signal_recorded():
    while True:
        current_time = time.time()
        expiration_time = 39 * 60  # 15 минут (или другой интервал, который вам нужен)
        for symbol, timestamp in list(signal_recorded.items()):
            if current_time - timestamp > expiration_time:
                del signal_recorded[symbol]
        time.sleep(300)  # Проверка каждые 5 минут


def filter_signal(sym):
    return sym not in signal_recorded


if __name__ == '__main__':
    signal_recorded = {} # Инициализируем словарь для отслеживания состояния каждого актива и метку времени

    cleaner_thread = threading.Thread(target=clean_signal_recorded) # Создаем и запускаем поток для удаления устаревших записей
    cleaner_thread.daemon = True
    cleaner_thread.start()

    createTxtFile('signal_vol.txt') # Создаем файлы для оповещения по сигналу

    start_time = time.time()

    while True:
        # try:
            symb_index = get_symbolPrice_ticker()
            index_sym = [symb['symbol'] for symb in symb_index if symb['symbol'].endswith('USDT')]
            print(len(index_sym))

            index_filtered = list(filter(filter_signal, index_sym))
            process = list(map(run_process, index_filtered))

            end_time = time.time()

            elapsed_time = end_time - start_time
            print(f"Время выполнения бесконечного цикла: {elapsed_time} секунд")

        # except Exception as e:
        #     print("Возникла непредвиденная ошибка.")
        #     time.sleep(5)

            time.sleep(60)
