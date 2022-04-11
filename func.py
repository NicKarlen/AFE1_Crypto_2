from upbit.client import Upbit
import requests
import json
from datetime import datetime, timedelta

"""
    Upbit: Upbit-client do get the 1 minute candle for the tradingpair
"""
def get_1min_Upbit(tradingpair):
    client = Upbit()
    resp = client.Candle.Candle_minutes(
        unit=1, # 1-min. candle
        market= tradingpair, # 'KRW-BTC', #Traingpair
        count= 1   # 60 candles
        #to="2022-04-10 16:00:00"  #yyyy-MM-dd HH:mm:ss
    )

    return {
        "tradingpair": resp['result'][0]['market'],
        "timestamp": resp['result'][0]['candle_date_time_utc'][:10] + ' ' + resp['result'][0]['candle_date_time_utc'][11:],
        "price_low": resp['result'][0]['low_price'],
        "price_high": resp['result'][0]['high_price'],
        "price_close": resp['result'][0]['trade_price'],
        "volume": resp['result'][0]['candle_acc_trade_volume']
    }


"""
    Coinbase: get the 1 minute candle for the tradingpair
"""
def get_1min_Coinbase(tradingpair):

    url = f"https://api.exchange.coinbase.com/products/{tradingpair}/candles?granularity=60"
    req = requests.get(url)
    json_response = json.loads(req.text)

    return {
        "tradingpair": tradingpair,
        "timestamp": str(datetime.fromtimestamp(json_response[0][0])),
        "price_low": json_response[0][1],
        "price_high": json_response[0][2],
        "price_close": json_response[0][4],
        "volume": json_response[0][5]
    }

"""
    Bitpanda: get the 1 minute candle for the tradingpair
"""
def get_1min_Bitpanda(tradingpair):

    t_now = datetime.utcnow()
    t_15min_ago = t_now - timedelta(minutes=15)

    dict_t_now = {
        # "year": str(t_now.year),
        # "month": str(t_now.month) if len(str(t_now.month)) == 2 else "0" + str(t_now.month),
        # "day": str(t_now.day) if len(str(t_now.day)) == 2 else "0" + str(t_now.day),
        "date":  str(t_now.date()),
        "hour": str(t_now.hour) if len(str(t_now.hour)) == 2 else "0" + str(t_now.hour),
        "minute": str(t_now.minute) if len(str(t_now.minute)) == 2 else "0" + str(t_now.minute)
    }
    dict_t_15min_ago = {
        # "year": str(t_15min_ago.year),
        # "month": str(t_15min_ago.month) if len(str(t_15min_ago.month)) == 2 else "0" + str(t_15min_ago.month),
        # "day": str(t_15min_ago.day) if len(str(t_15min_ago.day)) == 2 else "0" + str(t_15min_ago.day),
        "date":  str(t_15min_ago.date()),
        "hour": str(t_15min_ago.hour) if len(str(t_15min_ago.hour)) == 2 else "0" + str(t_15min_ago.hour),
        "minute": str(t_15min_ago.minute) if len(str(t_15min_ago.minute)) == 2 else "0" + str(t_15min_ago.minute)
    }

    print(dict_t_now)
    print(dict_t_15min_ago)

    #url = f"https://api.exchange.bitpanda.com/public/v1/candlesticks/{tradingpair}?unit=MINUTES&period=1&from={dict_t_15min_ago["year"]}-{dict_t_15min_ago[]}-11T04%3A59%3A59.999Z&to=2022-04-11T07%3A59%3A59.999Z"
    
    
    # req = requests.get(url)
    # json_response = json.loads(req.text)

    # return {
    #     "tradingpair": tradingpair,
    #     "timestamp": str(datetime.fromtimestamp(json_response[0][0])),
    #     "price_low": json_response[0][1],
    #     "price_high": json_response[0][2],
    #     "price_close": json_response[0][4],
    #     "volume": json_response[0][5]
    # }


# def calc_VWAP(dict_1min_candle):
#     pass