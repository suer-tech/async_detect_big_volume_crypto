import asyncio
import datetime
import threading
import time
import aiohttp

from bin_api import get_buy_sell_ratio, get_symbol_ticker
from calculate import calculate_average_vol, calculate_all_kline_high_percent, calculate_median_kline_high, \
    check_last_vol_on_average_vol
from config import timefraim, limit, median_x
from signals import create_new_signal, filter_recorded_signal, clean_signal_records
from utility import convert_time


params = {}

async def run_process(session, sym, all_ticker_list):
    params = {
        "symbol": sym,
        "period": timefraim,
        "limit": limit,
    }

    try:
        volume_ratio = await get_buy_sell_ratio(session, params)
        if len(volume_ratio) == limit:
            last_volume = volume_ratio[-2]
            average_volume = await calculate_average_vol(
                volume_ratio)
            checked_last_volume = await check_last_vol_on_average_vol(average_volume, last_volume)

            if checked_last_volume:
                params = {
                    "symbol": sym,
                    "interval": timefraim,
                    "limit": limit,
                }
                all_kline_high = await calculate_all_kline_high_percent(session,
                                                                        params)

                if all_kline_high:
                    last_kline_high = all_kline_high[-2]
                    value_last_kline_high = next(iter(last_kline_high.values()))
                    mediana = await calculate_median_kline_high(all_kline_high)

                    if mediana * median_x > float(value_last_kline_high):
                        this_time = datetime.datetime.now()
                        time_signal = datetime.datetime.strptime(await convert_time(last_volume['timestamp']),
                                                                 "%Y-%m-%d %H:%M:%S %Z")

                        t_vol = this_time - time_signal

                        # Сигнал большого обьема----------------------------
                        if t_vol.total_seconds() <= 45000:  # 900 секунд = 15 минут

                            for ticker in all_ticker_list:
                                if ticker['symbol'] == sym:
                                    await create_new_signal(ticker)
                            print(sym)


    except ZeroDivisionError as err:
        print('ZeroDivisionError')
        return None
    except IndexError as err:
        print('IndexError ')
        return None


async def main():
    start_time = time.time()

    while True:
        try:
            all_ticker_list = await get_symbol_ticker()
            usdt_ticker_list = [ticker['symbol'] for ticker in all_ticker_list if ticker['symbol'].endswith('USDT')]
            print(len(usdt_ticker_list))

            ticker_list = list(filter(filter_recorded_signal, usdt_ticker_list))

            async with aiohttp.ClientSession() as session:
                tasks = [run_process(session, ticker, all_ticker_list) for ticker in ticker_list]
                task_list = [asyncio.create_task(task) for task in tasks]
                await asyncio.gather(*task_list)

        except Exception as e:
            print("Возникла непредвиденная ошибка.")
            await asyncio.sleep(5)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время выполнения бесконечного цикла: {elapsed_time} секунд")

        await asyncio.sleep(360)


if __name__ == '__main__':
    cleaner_thread = threading.Thread(target=clean_signal_records)
    cleaner_thread.daemon = True
    cleaner_thread.start()

    asyncio.run(main())
