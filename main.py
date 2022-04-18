import func
import DB_func

# DB_func.create_fx_rate_table()
# DB_func.create_1min_candle_table()

dict_1min_candles_org = []
dict_1min_candles_org.append(func.get_1min_Upbit("KRW-BTC"))
dict_1min_candles_org.append(func.get_1min_Coinbase("BTC-USD"))
dict_1min_candles_org.append(func.get_1min_Bitstamp("btceur"))
print(dict_1min_candles_org[0])
print(dict_1min_candles_org[1])
print(dict_1min_candles_org[2])

# dict_FX_rate = func.get_FX_exchange_rate("EUR","USD", rate_dezimal_too_long=False)
# DB_func.write_FX_rate(dict_FX_rate)

# dict_FX_rate = func.get_FX_exchange_rate("KRW","USD", rate_dezimal_too_long=True)
# DB_func.write_FX_rate(dict_FX_rate)

# Calculate the average price and the vwap for the min (price*volume)
dict_1min_candles = []
#print(dict_1min_candles_org)
for candle in dict_1min_candles_org:
    
    dict_1min_candles.append(func.calc_avg_price_and_vwap1min(candle))

print(dict_1min_candles)
