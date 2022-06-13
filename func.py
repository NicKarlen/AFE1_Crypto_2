# from upbit.client import Upbit
import requests
import json
from datetime import datetime, timedelta
import DB_func
import logging

"""
    We always take the 1-minute candle that is 1 min ago. 
    If we take the latest, the candle is still developing (not done yet)
"""
# Upbit-client pip: https://pypi.org/project/upbit-client/ . Used to get the 1 minute candle for the tradingpair
# 20.04.2022: Upbit-Client is not used anymore because of errors!!!

# Upbit: get the 1 minute candle for the tradingpair
def get_1min_Upbit(tradingpair):
    
    url = f"https://api.upbit.com/v1/candles/minutes/1?market={tradingpair}&count=2"
    req = requests.get(url)
    json_response = json.loads(req.text)

    # index to read from the exchange response
    index = 1

    # adjust timestamp from Upbit
    timestamp = datetime.fromisoformat(json_response[index]["candle_date_time_utc"]) + timedelta(hours=2)
    timestamp0 = datetime.fromisoformat(json_response[0]["candle_date_time_utc"]) + timedelta(hours=2)

    #  if the timestamp of the requested data is not equal the prior minute we assume that the
    #  tradingvolume in that minute was 0 and we therefore set the timestamp to the current time
    #  and the volume to 0 so it won't be considered in the calculation of the arbitrage index
    #  and the script keeps running.
    now = timestamp.now().replace(microsecond=0, second=0)
    now_1min_ago = now - timedelta(minutes=1)
    if timestamp != now_1min_ago :
        # We check if the latest timestamp matches the one from 1 minute ago. 
        # if yes we will take the data from this candle, because we assume that the new candle has not opend yet.
        if timestamp0 == now_1min_ago:
            timestamp = str(now_1min_ago)
            index = 0
            logging.warning('Upbit: new candle did not yet open... - tradingpair: %s   Timestamp now_1min_ago: %s', tradingpair, str(timestamp))
            logging.warning("json_response:")
            logging.warning(json_response)
            volume = float(json_response[index]['candle_acc_trade_volume'])
        else:
            timestamp = str(now_1min_ago)
            volume = 0
            logging.warning('Upbit: timestamp was not equal - tradingpair: %s  Timestamp  now_1min_ago: %s', tradingpair, str(timestamp))
            logging.warning("json_response:")
            logging.warning(json_response)
    else:
        volume = float(json_response[index]['candle_acc_trade_volume'])

    return {
        "tradingpair": json_response[index]['market'],
        "exchange": "Upbit",
        "timestamp": str(timestamp),
        "price_low": float(json_response[index]['low_price']),
        "price_high": float(json_response[index]['high_price']),
        "price_close": float(json_response[index]['trade_price']),
        "volume": volume
    }


# Coinbase: get the 1 minute candle for the tradingpair
def get_1min_Coinbase(tradingpair):

    url = f"https://api.exchange.coinbase.com/products/{tradingpair}/candles?granularity=60"
    req = requests.get(url)
    json_response = json.loads(req.text)

    # read timestamp
    timestamp = datetime.fromtimestamp(json_response[1][0])

    #  if the timestamp of the requested data is not equal the prior minute we assume that the
    #  tradingvolume in that minute was 0 and we there for set the timestamp to the current time
    #  and the volume to 0 so it won't be considered in the calculation of the arbitrage index
    #  and the script keeps running.
    now = timestamp.now().replace(microsecond=0, second=0)
    now_1min_ago = now - timedelta(minutes=1)
    if timestamp != now_1min_ago :
        timestamp = str(now_1min_ago)
        volume = 0
        logging.warning('Coinbase: timestamp was not equal - tradingpair: %s  Timestamp  now_1min_ago: %s', tradingpair, str(timestamp))
        logging.warning("json_response:")
        logging.warning(json_response)
    else:
        volume = float(json_response[1][5])

    return {
        "tradingpair": tradingpair,
        "exchange": "Coinbase",
        "timestamp": str(timestamp),
        "price_low": float(json_response[1][1]),
        "price_high": float(json_response[1][2]),
        "price_close": float(json_response[1][4]),
        "volume": volume
    }


# Bitstamp: get 1 minute candle from the given tradingpair
def get_1min_Bitstamp(tradingpair):

    url = f"https://www.bitstamp.net/api/v2/ohlc/{tradingpair}/?step=60&limit=2"
    req = requests.get(url)
    json_response = json.loads(req.text)

    # read and adjust timestamp
    timestamp = datetime.fromtimestamp(int(json_response["data"]["ohlc"][0]["timestamp"]))

    #  if the timestamp of the requested data is not equal the prior minute we assume that the
    #  tradingvolume in that minute was 0 and we there for set the timestamp to the current time
    #  and the volume to 0 so it won't be considered in the calculation of the arbitrage index
    #  and the script keeps running.
    now = timestamp.now().replace(microsecond=0, second=0)
    now_1min_ago = now - timedelta(minutes=1)
    if timestamp != now_1min_ago :
        timestamp = str(now_1min_ago)
        volume = 0
        logging.warning('Bitstamp: timestamp was not equal - tradingpair: %s  Timestamp  now_1min_ago: %s', tradingpair, str(timestamp))
        logging.warning("json_response:")
        logging.warning(json_response)
    else:
        volume = float(json_response["data"]["ohlc"][0]["volume"])

    return {
        "tradingpair": json_response["data"]["pair"][:3] + "-" + json_response["data"]["pair"][4:],
        "exchange": "Bitstamp",
        "timestamp": str(timestamp),
        "price_low": float(json_response["data"]["ohlc"][0]["low"]),
        "price_high": float(json_response["data"]["ohlc"][0]["high"]),
        "price_close": float(json_response["data"]["ohlc"][0]["close"]),
        "volume": volume
    }


# Get the current FX exchange rates for KRW -> USD and EUR -> USD
# Old FX API
def get_FX_exchange_rate_old(base, quote, rate_dezimal_too_long):

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

# Get the current FX exchange rates for KRW -> USD and EUR -> USD
# New FX API
def get_FX_exchange_rate_new(base, quote):

    api_key = "008e6b12db4078b631c34abd"
    
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{quote}"
    req = requests.get(url)
    json_response = json.loads(req.text)
    rate = float(json_response["conversion_rate"])

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

    if candle["tradingpair"].find('KRW') != -1:
        latest_FX_rate = DB_func.read_FX_rate("KRW-USD")[0]
    elif candle["tradingpair"].find('EUR') != -1:
        latest_FX_rate = DB_func.read_FX_rate("EUR-USD")[0]
    else:
        latest_FX_rate = 1

    candle["FX_rate"] = latest_FX_rate
    candle["price_low_USD"] = round(candle["price_low"] * latest_FX_rate, 6)
    candle["price_high_USD"] = round(candle["price_high"] * latest_FX_rate, 6)
    candle["price_close_USD"] = round(candle["price_close"] * latest_FX_rate, 6)

    return candle

# Calculate the average price and the vwap for the min (price*volume)
def calc_avg_price_and_vwap1min(candle_org):
    candle = candle_org
    
    # Average price is calc by adding price_low, price_high and price_close divided by 3
    candle["avg_price_USD"] = round((candle["price_low_USD"] + candle["price_high_USD"] + candle["price_close_USD"]) / 3, 6)

    candle["VWAP_1min"] = round(candle["avg_price_USD"] * candle["volume"], 6)

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
    
    # Division by 0
    if sum_VWAP1min == 0 or sum_volume1min == 0:
        moving_avg_VWAP_1h = 1
    else:
        moving_avg_VWAP_1h = round(sum_VWAP1min/sum_volume1min, 6)

    return {
        "tradingpair" : arr_data_last_hour[0][0],
        "timestamp" : arr_data_last_hour[0][1],
        "exchange" : arr_data_last_hour[0][2],
        "moving_avg_VWAP1h" : moving_avg_VWAP_1h,
        "timestamp_from" : arr_data_last_hour[59][1],
        "timestamp_to" : arr_data_last_hour[0][1]
    }

# Calculate the arbitrage index form the moving avg. of the VWAP_1h
def calc_arb_idx(base):

    # SELECT tradingpair, timestamp, exchange, moving_avg_VWAP1h, timestamp_from, timestamp_to
    #           0           1           2               3                4           5          
    arr_latest_VWAP1h = DB_func.read_Moving_avg_VWAP1h(base)
    
    min_VWAP1h = min(arr_latest_VWAP1h[0][3], arr_latest_VWAP1h[1][3], arr_latest_VWAP1h[2][3])
    max_VWAP1h = max(arr_latest_VWAP1h[0][3], arr_latest_VWAP1h[1][3], arr_latest_VWAP1h[2][3])

    arb_idx = round(max_VWAP1h / min_VWAP1h, 6)

    return {
        "commen_currency" : base,
        "timestamp" : arr_latest_VWAP1h[0][1],
        "exchanges" : arr_latest_VWAP1h[0][2] + "/" + arr_latest_VWAP1h[1][2] + "/" + arr_latest_VWAP1h[2][2],
        "VWAP_1h_min" : min_VWAP1h,
        "VWAP_1h_max" : max_VWAP1h,
        "arbitrage_index" : arb_idx
    }

    











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

   
