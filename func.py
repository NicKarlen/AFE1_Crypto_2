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
        #"timestamp": resp['result'][0]['candle_date_time_utc'][:10] + ' ' + resp['result'][0]['candle_date_time_utc'][11:],
        "timestamp": str(datetime.fromtimestamp(int(str(resp["result"][0]["timestamp"])[:10]))),
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
    Bitstamp: get 1 minute candle from the given tradingpair
"""

def get_1min_Bitstamp(tradingpair):

    url = f"https://www.bitstamp.net/api/v2/ohlc/{tradingpair}/?step=60&limit=1"
    req = requests.get(url)
    json_response = json.loads(req.text)

    return {
        "tradingpair": json_response["data"]["pair"][:3] + "-" + json_response["data"]["pair"][4:],
        "timestamp": str(datetime.fromtimestamp(int(json_response["data"]["ohlc"][0]["timestamp"]))),
        "price_low": json_response["data"]["ohlc"][0]["low"],
        "price_high": json_response["data"]["ohlc"][0]["high"],
        "price_close": json_response["data"]["ohlc"][0]["close"],
        "volume": json_response["data"]["ohlc"][0]["volume"]
    }


"""
    Bitpanda: get the 1 minute candle for the tradingpair

    WAS NOT USED. VOLUME ON EXCHANGE IS TO LOW: 
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

    url = f'https://api.exchange.bitpanda.com/public/v1/candlesticks/{tradingpair}?unit=MINUTES&period=1&from={dict_t_15min_ago["date"]}T{dict_t_15min_ago["hour"]}%3A{dict_t_15min_ago["minute"]}%3A59.999Z&to={dict_t_now["date"]}T{dict_t_now["hour"]}%3A{dict_t_now["minute"]}%3A59.999Z'
    
    print(url)
    
    req = requests.get(url)
    json_response = json.loads(req.text)

    print(json_response)



# def calc_VWAP(dict_1min_candle):
#     pass