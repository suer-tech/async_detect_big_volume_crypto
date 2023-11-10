currencies = [{
    'name': 'USD/RUB',
    'url': "https://ru.investing.com/currencies/usd-rub",
    'xpath': '//span[@class="text-2xl"]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div/div/div/main/div/div[1]/div[2]/div[1]/div[2]/span[2]',
},
{
    'name': 'EUR/RUB',
    'url': "https://ru.investing.com/currencies/eur-rub",
    'xpath': '//span[@class="text-2xl"]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div/div/div/main/div/div[1]/div[2]/div[1]/div[2]/span[2]',

},
{
    'name': 'CNY/RUB',
    'url': "https://ru.investing.com/currencies/cny-rub",
    'xpath': '//span[@class="text-2xl"]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div/div/div/main/div/div[1]/div[2]/div[1]/div[2]/span[2]',
},

]

comodities = [{
    'name': 'Золото',
    'url': "https://ru.investing.com/commodities/gold",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',

},
{
    'name': 'Нефть BRENT',
    'url': "https://ru.investing.com/commodities/brent-oil",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
},
{
    'name': 'Natural GAS',
    'url': "https://ru.investing.com/commodities/natural-gas",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'day': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'year': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[5]/div[1]/dl[1]/div[5]/dd/span/span[2]',
},
]

index = [{
    'name': 'Индекс Мосбиржи',
    'url': "https://ru.investing.com/indices/mcx",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
},
{
    'name': 'S&P 500',
    'url': "https://ru.investing.com/indices/us-spx-500",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
},
{
    'name': 'DAX',
    'url': "https://ru.investing.com/indices/germany-30",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'day': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'year': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[5]/div[1]/dl[1]/div[5]/dd/span/span[2]',
},
{
    'name': 'Shanghai Composite',
    'url': "https://ru.investing.com/indices/shanghai-composite",
    'xpath': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]',
    'xpath_proc': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'day': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[2]/span[2]',
    'year': '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[5]/div[1]/dl[1]/div[5]/dd/span/span[2]',
},
]