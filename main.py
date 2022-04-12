import func
import DB_func

# DB_func.create_fx_rate_table()
# DB_func.create_1min_candle_table()

# dict_1min_candles = {}
# dict_1min_candles["Upbit"] = func.get_1min_Upbit("KRW-BTC")
# dict_1min_candles["Coinbase"] = func.get_1min_Coinbase("BTC-USD")
# dict_1min_candles["Bitstamp"] = func.get_1min_Bitstamp("btceur")
# print(dict_1min_candles["Upbit"])
# print(dict_1min_candles["Coinbase"])
# print(dict_1min_candles["Bitstamp"])

dict_FX_rate = func.get_FX_exchange_rate("EUR","USD", rate_dezimal_too_long=False)
DB_func.write_FX_rate(dict_FX_rate)

dict_FX_rate = func.get_FX_exchange_rate("KRW","USD", rate_dezimal_too_long=True)
DB_func.write_FX_rate(dict_FX_rate)