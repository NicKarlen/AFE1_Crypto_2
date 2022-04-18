from upbit.client import Upbit
import requests
import json
from datetime import datetime, timedelta



"""
    We always take the 1-minute candle that is 1 min ago. If we take the latest, the candle is still developing (not done yet)

    Upbit: Upbit-client do get the 1 minute candle for the tradingpair
"""
def get_1min_Upbit(tradingpair):
    client = Upbit()
    resp = client.Candle.Candle_minutes(
        unit=1, # 1-min. candle
        market= tradingpair, # 'KRW-BTC', #Traingpair
        count= 2   # 60 candles
        #to="2022-04-10 16:00:00"  #yyyy-MM-dd HH:mm:ss
    )

    return {
        "tradingpair": resp['result'][1]['market'],
        "exchange": "Upbit",
        "timestamp": str(datetime.fromtimestamp(int(str(resp["result"][1]["timestamp"])[:10]))),
        "price_low": float(resp['result'][1]['low_price']),
        "price_high": float(resp['result'][1]['high_price']),
        "price_close": float(resp['result'][1]['trade_price']),
        "volume": float(resp['result'][1]['candle_acc_trade_volume'])
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
        "exchange": "Coinbase",
        "timestamp": str(datetime.fromtimestamp(json_response[1][0])),
        "price_low": float(json_response[1][1]),
        "price_high": float(json_response[1][2]),
        "price_close": float(json_response[1][4]),
        "volume": float(json_response[1][5])
    }




"""
    Bitstamp: get 1 minute candle from the given tradingpair
"""
def get_1min_Bitstamp(tradingpair):

    url = f"https://www.bitstamp.net/api/v2/ohlc/{tradingpair}/?step=60&limit=2"
    req = requests.get(url)
    json_response = json.loads(req.text)

    return {
        "tradingpair": json_response["data"]["pair"][:3] + "-" + json_response["data"]["pair"][4:],
        "exchange": "Bitstamp",
        "timestamp": str(datetime.fromtimestamp(int(json_response["data"]["ohlc"][0]["timestamp"]))),
        "price_low": float(json_response["data"]["ohlc"][0]["low"]),
        "price_high": float(json_response["data"]["ohlc"][0]["high"]),
        "price_close": float(json_response["data"]["ohlc"][0]["close"]),
        "volume": float(json_response["data"]["ohlc"][0]["volume"])
    }



"""
    Get the current FX exchange rates for KRW -> USD and EUR -> USD
"""
def get_FX_exchange_rate(base, quote, rate_dezimal_too_long):

    api_key = "529ea55ae0ef21448defc7955877504d06729ff4"

    # The API only returns 5 decimal places and therefore when the conversion rate is very
    # small you have to get the inverse conversion rate and calc 1/conversion-rate-inverse to get a semi accurate rate

    if rate_dezimal_too_long:
        url = f"https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}&from={quote}&to={base}&format=json"
        req = requests.get(url)
        json_response = json.loads(req.text)
        rate = 1 / float(json_response["rates"][base]["rate"])

    else:
        url = f"https://api.getgeoapi.com/v2/currency/convert?api_key={api_key}&from={base}&to={quote}&format=json"
        req = requests.get(url)
        json_response = json.loads(req.text)
        rate = float(json_response["rates"][quote]["rate"])

    return {
        "tradingpair": base + "-" + quote,
        "timestamp": str(datetime.now()),
        "base": base,
        "quote": quote,
        "rate_base_to_quote": rate
    }


def recalc_price_in_USD():
    pass

# Calculate the average price and the vwap for the min (price*volume)
def calc_avg_price_and_vwap1min(candle_org):
    candle = candle_org
    
    # Average price is calc by adding price_low, price_high and price_close divided by 3
    candle["avg_price"] = (candle["price_low"] + candle["price_high"] + candle["price_close"]) / 3

    candle["VWAP_1min"] = candle["avg_price"] * candle["volume"]

    return candle


    



"""
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

    url = f'https://api.exchange.bitpanda.com/public/v1/candlesticks/{tradingpair}?unit=MINUTES&period=1&from={dict_t_15min_ago["date"]}T{dict_t_15min_ago["hour"]}%3A{dict_t_15min_ago["minute"]}%3A59.999Z&to={dict_t_now["date"]}T{dict_t_now["hour"]}%3A{dict_t_now["minute"]}%3A59.999Z'

    req = requests.get(url)
    json_response = json.loads(req.text)

   
