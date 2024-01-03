import requests

# Binance API endpoint for top gainers and losers



def get_symbolPrice_ticker():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error occurred while retrieving Kline data:", response.text)
        return None

def get_gainers(sym, gainers, losers):
    api_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    # Fetch the top gainers
    params = {
        "symbol": sym,  # Change the symbol to your preferred trading pair
        "sort": "percent_change",
        "limit": 10
    }
    response = requests.get(api_url, params=params)
    item = response.json()
    if float(item['priceChangePercent']) > 0:
        gainers.append(item)
    if float(item['priceChangePercent']) < 0:
        losers.append(item)
        

def get_top_gainers():
    leaders = []
    api_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    # Fetch the top gainers
    params = {
        "symbol": 'BTCUSDT',  # Change the symbol to your preferred trading pair
        "sort": "percent_change",
        "limit": 10
    }
    response = requests.get(api_url, params=params)
    item = response.json()
    leaders.append(item)

    params = {
        "symbol": 'ETHUSDT',  # Change the symbol to your preferred trading pair
        "sort": "percent_change",
        "limit": 10
    }
    response = requests.get(api_url, params=params)
    item = response.json()
    leaders.append(item)
    return leaders
        

def get_crypto():
    
    top = get_top_gainers()
    with open('crypto.txt', 'w') as file:
        file.write("Крипто:\n")

    # Выведите топ 10 прибыльных пар
    for t in top:
        # Открываем файл для записи
        with open('crypto.txt', 'a') as file:
            if float(t['priceChangePercent']) > 0:
                file.write(f"{t['symbol'][:-4]}: {t['lastPrice']}  +{float(t['priceChangePercent']):.2f}%\n")
            else:
                file.write(f"{t['symbol'][:-4]}: {t['lastPrice']}  {float(t['priceChangePercent']):.2f}%\n")

    index = []
    symb_index = get_symbolPrice_ticker()
    for symb in symb_index:
        if symb['symbol'].endswith('USDT'):
            index.append(symb['symbol'])

    gainers = []
    losers = []

    for x in index:
        get_gainers(x, gainers, losers)

    top_gainers = sorted(gainers, key=lambda x: float(x['priceChangePercent']), reverse=True)[:5]

    with open('crypto.txt', 'a') as file:
        file.write("\nЛидеры роста:\n")

    # Выведите топ 10 прибыльных пар
    for gainer in top_gainers:
        # Открываем файл для записи
        with open('crypto.txt', 'a') as file:
            file.write(f"{gainer['symbol'][:-4]}: {gainer['lastPrice']}  +{float(gainer['priceChangePercent']):.2f}%\n")
       

    top_losers = sorted(losers, key=lambda x: float(x['priceChangePercent']))[:5]

    with open('crypto.txt', 'a') as file:
        file.write("\nЛидеры падения:\n")

    # Выведите топ 10 прибыльных пар
    for loser in top_losers:
        # Открываем файл для записи
        with open('crypto.txt', 'a') as file:
            file.write(f"{loser['symbol'][:-4]}: {loser['lastPrice']}  {float(loser['priceChangePercent']):.2f}%\n")

