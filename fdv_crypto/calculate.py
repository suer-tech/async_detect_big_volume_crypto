from statistics import median
from bin_api import get_kline_data
from config import buy_sell_ratio_x


async def calculate_all_kline_high_percent(session, params):
    kline_data = await get_kline_data(session, params)
    if kline_data:
        result = [
            {k[0]: round((float(k[2]) - float(k[3])) / float(k[2]) * 100, 4)}
            for k in kline_data
        ]
        return result


async def calculate_median_kline_high(data_list):
    values = [float(list(item.values())[0]) for item in data_list]
    return median(values)


async def calculate_average_vol(data):
    total_buy_vol = sum([float(item['buyVol']) for item in data])
    total_sell_vol = sum([float(item['sellVol']) for item in data])

    num_items = len(data)
    mean_buy_vol = total_buy_vol / num_items
    mean_sell_vol = total_sell_vol / num_items

    average_vol_list = [mean_buy_vol, mean_sell_vol]
    return average_vol_list


async def check_last_vol_on_average_vol(average_vol_list, ratio_last):
    buy_vol = float(ratio_last['buyVol'])
    sell_vol = float(ratio_last['sellVol'])
    diff = buy_sell_ratio_x
    if buy_vol > average_vol_list[0] * diff or sell_vol > average_vol_list[1] * diff:
        return ratio_last
