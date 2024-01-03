import aiohttp


async def get_symbol_ticker():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print("Error occurred while retrieving Kline data:", response.text)
                return None


async def get_buy_sell_ratio(session, params):
    url = "https://fapi.binance.com/futures/data/takerlongshortRatio"
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print("Error occurred while retrieving Kline data:", await response.text)
            return None


# Запрос свечек с биржи-----------------------------------------------------------------------------
async def get_kline_data(session, params):
    url = "https://fapi.binance.com/fapi/v1/klines"
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print("Error occurred while retrieving Kline data:", response.text)
            return None