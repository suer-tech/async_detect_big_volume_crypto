import asyncio
import os

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from keyboard import greet_kb1

token = '6419893616:AAG-tbu524ZN7IGIulbJA_ZxNLykdaJWeU0'
bot = Bot(token)
from aiogram import Dispatcher

users_id = [412850740, 878760195]


async def send_message(txt_file):
    if os.stat(txt_file).st_size > 0:
        with open(txt_file, 'r', encoding='utf-8') as fr:
            mess = fr.read()
        for user in users_id:
            try:
                await bot.send_message(user, mess)
            except Exception as e:
                print(f"Error sending message to user {user}: {str(e)}")

        await remove_message_file(txt_file)


async def remove_message_file(txt_file):
    os.remove(txt_file)


async def polling_thread():
    while True:
        for file_name in os.listdir('..fast_detect_volume_crypto'):
            if file_name.endswith('_signal.txt'):
                await send_message(file_name)
                await asyncio.sleep(1)


async def process_start_command(message: types.Message):
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDZ2JEZuGR8N1D5s__y0O8cIUGMk9OAAIiEwACXWxwS64th70744A-IwQ')
    mess = f'Привет, <b>{message.from_user.first_name}</b>! Здесь будут уведомления об изменении цены по основным биржевым активам.'
    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=greet_kb1)


async def with_puree(message: types.Message, file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            mess = data if data else f"Нет данных"
        await bot.send_message(message.chat.id, mess, reply_markup=greet_kb1)
    except FileNotFoundError:
        await bot.send_message(message.chat.id, f"Файл не найден")
    except Exception as e:
        await bot.send_message(message.chat.id, f"Произошла ошибка при чтении файла: {str(e)}")


if __name__ == "__main__":
    dp = Dispatcher(bot)

    # Запуск асинхронного потока для отправки сообщений
    loop = asyncio.get_event_loop()
    loop.create_task(polling_thread())

    # Обработчики сообщений
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(lambda message: with_puree(message, "../parser/output.txt"), Text(equals="Индексы"))
    dp.register_message_handler(lambda message: with_puree(message, "../parser/crypto.txt"), Text(equals="Крипто"))
    dp.register_message_handler(lambda message: with_puree(message, "../moex/all_spread.txt"), Text(equals="Спреды"))

    # Запуск бота
    executor.start_polling(dp, loop=loop)
