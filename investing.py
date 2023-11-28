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
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',

},
{
    'name': 'Нефть BRENT',
    'url': "https://ru.investing.com/commodities/brent-oil",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',
},
{
    'name': 'Natural GAS',
    'url': "https://ru.investing.com/commodities/natural-gas",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',

},
]

index = [{
    'name': 'Индекс Мосбиржи',
    'url': "https://ru.investing.com/indices/mcx",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',
},
{
    'name': 'S&P 500',
    'url': "https://ru.investing.com/indices/us-spx-500",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',
},
{
    'name': 'DAX',
    'url': "https://ru.investing.com/indices/germany-30",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',

},
{
    'name': 'Shanghai Composite',
    'url': "https://ru.investing.com/indices/shanghai-composite",
    'xpath': '//span[@data-test="instrument-price-last"]',
    'xpath_proc': '//span[@data-test="instrument-price-change-percent"]',

},
]