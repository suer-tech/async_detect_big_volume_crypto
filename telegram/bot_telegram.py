import asyncio
import os

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from keyboard import greet_kb1
from telegram.tg_config import users_id, token, fdv_crypto_dir_path, parser_dir_path, moex_dir_path

from aiogram import Dispatcher
bot = Bot(token)


async def send_message(full_path):
    file = full_path
    if os.stat(file).st_size > 0:
        with open(file, 'r', encoding='utf-8') as fr:
            mess = fr.read()
        for user in users_id:
            try:
                await bot.send_message(user, mess)
            except Exception as e:
                print(f"Error sending message to user {user}: {str(e)}")

        await remove_message_file(full_path)


async def remove_message_file(full_path):
    os.remove(full_path)


async def polling_thread():
    while True:
        await asyncio.sleep(1)
        for file_name in os.listdir(fdv_crypto_dir_path):
            full_path = os.path.join(fdv_crypto_dir_path, file_name)
            if file_name.endswith('_signal.txt'):
                await send_message(full_path)


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
    index_file_full_path = os.path.join(parser_dir_path, 'output.txt')
    dp.register_message_handler(lambda message: with_puree(message, index_file_full_path), Text(equals="Индексы"))
    crypto_file_full_path = os.path.join(parser_dir_path, 'crypto.txt')
    dp.register_message_handler(lambda message: with_puree(message, crypto_file_full_path), Text(equals="Крипто"))
    moex_file_full_path = os.path.join(moex_dir_path, 'all_spread.txt')
    dp.register_message_handler(lambda message: with_puree(message, moex_file_full_path), Text(equals="Спреды"))

    # Запуск бота
    executor.start_polling(dp, loop=loop)
