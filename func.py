from upbit.client import Upbit
import requests
import json
from datetime import datetime, timedelta
import DB_func



"""
    We always take the 1-minute candle that is 1 min ago. 
    If we take the latest, the candle is still developing (not done yet)
"""
# Upbit: Upbit-client do get the 1 minute candle for the tradingpair
def get_1min_Upbit(tradingpair):
    client = Upbit()
    resp = client.Candle.Candle_minutes(
        unit=1, # 1-min. candle
        market= tradingpair, # 'KRW-BTC', #Traingpair
        count= 2   # 60 candles
        #to="2022-04-10 16:00:00"  #yyyy-MM-dd HH:mm:ss
    )

    print(resp)
    timestamp = datetime.fromisoformat(resp["result"][1]["candle_date_time_utc"]) + timedelta(hours=2)

    return {
        "tradingpair": resp['result'][1]['market'],
        "exchange": "Upbit",
        "timestamp": str(timestamp),
        "price_low": float(resp['result'][1]['low_price']),
        "price_high": float(resp['result'][1]['high_price']),
        "price_close": float(resp['result'][1]['trade_price']),
        "volume": float(resp['result'][1]['candle_acc_trade_volume'])
    }


# Coinbase: get the 1 minute candle for the tradingpair
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


# Bitstamp: get 1 minute candle from the given tradingpair
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


# Get the current FX exchange rates for KRW -> USD and EUR -> USD
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


# recalc the prices in USD based on the latest FX exchange rate found in the database
def recalc_price_in_USD(candle_org):
    candle = candle_org

    if candle["tradingpair"] == "KRW-BTC":
        latest_FX_rate = DB_func.read_FX_rate("KRW-USD")[0]
    elif candle["tradingpair"] == "BTC-EUR":
        latest_FX_rate = DB_func.read_FX_rate("EUR-USD")[0]
    else:
        latest_FX_rate = 1

    candle["FX_rate"] = latest_FX_rate
    candle["price_low_USD"] = round(candle["price_low"] * latest_FX_rate, 2)
    candle["price_high_USD"] = round(candle["price_high"] * latest_FX_rate, 2)
    candle["price_close_USD"] = round(candle["price_close"] * latest_FX_rate, 2)

    return candle

# Calculate the average price and the vwap for the min (price*volume)
def calc_avg_price_and_vwap1min(candle_org):
    candle = candle_org
    
    # Average price is calc by adding price_low, price_high and price_close divided by 3
    candle["avg_price_USD"] = round((candle["price_low_USD"] + candle["price_high_USD"] + candle["price_close_USD"]) / 3, 2)

    candle["VWAP_1min"] = round(candle["avg_price_USD"] * candle["volume"], 2)

    return candle

# Calculate the VWAP_1h for the last 60min
def calc_VWAP_1h(tradingpair):
    sum_VWAP1min = 0
    sum_volume1min = 0

    # SELECT tradingpair, timestamp, exchange, volume, avg_price_USD, VWAP_1min
    #           0           1           2         3         4           5
    arr_data_last_hour = DB_func.read_One_Min_Candles(tradingpair)

    for ele in arr_data_last_hour:
        sum_VWAP1min += ele[5]
        sum_volume1min += ele[3]
    
    return {
        "tradingpair" : arr_data_last_hour[0][0],
        "timestamp" : arr_data_last_hour[0][1],
        "exchange" : arr_data_last_hour[0][2],
        "moving_avg_VWAP1h" : round(sum_VWAP1min/sum_volume1min, 2),
        "timestamp_from" : arr_data_last_hour[59][1],
        "timestamp_to" : arr_data_last_hour[0][1]
    }

# Calculate the arbitrage index form the moving avg. of the VWAP_1h
def calc_arb_idx():
    pass









# WAS NOT USED. VOLUME ON EXCHANGE IS TO LOW: 
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

   
