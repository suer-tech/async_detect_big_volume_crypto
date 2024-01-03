import time

import binance
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from investing import currencies, comodities, index
from crypto import get_crypto
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())


chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=service, options=chrome_options)

def get_price(name, url, xpath, xpath_proc):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    price = wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).text
    proc = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_proc))).text
    return [name, price, proc]


# Функция для форматирования чисел
def format_number(input_str):
    # Удаляем все знаки "."
    input_str = input_str.replace('.', '')

    # Заменяем "," на "."
    input_str = input_str.replace(',', '.')

    # Оставляем два знака после разделителя "."
    if '.' in input_str:
        parts = input_str.split('.')
        if len(parts) == 2:
            input_str = f"{parts[0]}.{parts[1][:2]}"

    return input_str


while True:
    try:

        curr_arr = []
        for curr in currencies:
            item = get_price(curr['name'], curr['url'], curr['xpath'], curr['xpath_proc'])
            curr_arr.append(item)

        print(curr_arr)

        comoditi_arr = []
        for comod in comodities:
            item = get_price(comod['name'], comod['url'], comod['xpath'], comod['xpath_proc'])
            comoditi_arr.append(item)

        print(comoditi_arr)

        index_arr = []
        for ind in index:
            item = get_price(ind['name'], ind['url'], ind['xpath'], ind['xpath_proc'])
            index_arr.append(item)

        print(index_arr)



        # Открываем файл для записи
        with open('output.txt', 'w') as file:
            file.write("Валюты:\n")
            for currency in curr_arr:
                formatted_value = format_number(currency[1])
                formatted_proc = format_number(currency[2])
                proc_without_brackets = formatted_proc.replace("(", "").replace(")", "")
                file.write(f"{currency[0]}: {formatted_value}  {proc_without_brackets}%\n")

            file.write("\nТовары:\n")
            for comodity in comoditi_arr:
                formatted_value = format_number(comodity[1])
                formatted_proc = format_number(comodity[2])
                proc_without_brackets = formatted_proc.replace("(", "").replace(")", "")
                file.write(f"{comodity[0]}: {formatted_value}  {proc_without_brackets}%\n")

            file.write("\nИндексы:\n")
            for ind in index_arr:
                formatted_value = format_number(ind[1])
                formatted_proc = format_number(ind[2])
                proc_without_brackets = formatted_proc.replace("(", "").replace(")", "")
                file.write(f"{ind[0]}: {formatted_value}  {proc_without_brackets}%\n")


        get_crypto()

    except Exception as e:
        print("Возникла непредвиденная ошибка.")
        time.sleep(5)

    time.sleep(900)


