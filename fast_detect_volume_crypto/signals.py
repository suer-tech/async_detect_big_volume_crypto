import time
import os
import aiofiles
import emoji

signal_records = {}


class Signal:
    def __init__(self, ticker):
        self.ticker = ticker['symbol']
        self.price = ticker['price']
        self.short = None
        self.long = None

    async def calculate_signal_instance(self):
        price = float(self.price)

        self.long = {
            '1 tvh': price,
            '2 tvh': price - price / 100 * 2,
            '3 tvh': price - price / 100 * 4,
            'stop': price - price / 100 * 5.5,
            'take': price + price / 100 * 2,
        }

        self.short = {
            '1 tvh': price,
            '2 tvh': price + price / 100 * 2,
            '3 tvh': price + price / 100 * 4,
            'stop': price + price / 100 * 5.5,
            'take': price - price / 100 * 2,
        }

    async def write_signal(self) -> None:
        try:
            async with aiofiles.open(f'{self.ticker}_signal', mode='r') as file:
                await file.read()

        except FileNotFoundError as err:
            async with aiofiles.open(f'{self.ticker}_signal', encoding='utf-8', mode='w') as file:
                mess = f"{emoji.emojize(':antenna_bars:Скачок объема торгов')}\n{emoji.emojize(':check_mark_button:')}{self.ticker}\n"
                await file.write(mess)
                await file.write(f"\nLong\n")

                for key, value in self.long.items():
                    await file.write(f"{key}: {value}\n")

                await file.write(f"\nShort\n")
                for key, value in self.short.items():
                    await file.write(f"{key}: {value}\n")


async def create_new_signal(ticker):
    new_signal = Signal(ticker)
    await new_signal.calculate_signal_instance()
    await new_signal.write_signal()
    signal_records[ticker['symbol']] = time.time()


def clean_signal_records():
    while True:
        current_time = time.time()
        expiration_time = 39 * 60
        keys_to_remove = []
        for symbol, timestamp in list(signal_records.items()):
            if current_time - timestamp > expiration_time:
                keys_to_remove.append(symbol)
        for key in keys_to_remove:
            del signal_records[key]
        time.sleep(300)


def filter_recorded_signal(ticker):
    return ticker not in signal_records
