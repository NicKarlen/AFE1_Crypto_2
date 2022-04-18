import func
import DB_func

""" Global variables """
dict_1min_candles_org = []
dict_1min_candles_in_USD = []
dict_1min_candles = []

""" Create database """
def step_0():
    DB_func.create_fx_rate_table()
    DB_func.create_1min_candle_table()

""" Get 1 min candle from the exchanges """
def step_1(): 
    dict_1min_candles_org.append(func.get_1min_Upbit("KRW-BTC"))
    dict_1min_candles_org.append(func.get_1min_Coinbase("BTC-USD"))
    dict_1min_candles_org.append(func.get_1min_Bitstamp("btceur"))
    # print(dict_1min_candles_org[0])
    # print(dict_1min_candles_org[1])
    # print(dict_1min_candles_org[2])


""" Get the exchange rate for the FX pairs needed (EUR-USD & KRW-USD) """
def step_2():
    dict_FX_rate = func.get_FX_exchange_rate("EUR","USD", rate_dezimal_too_long=False)
    DB_func.write_FX_rate(dict_FX_rate)

    dict_FX_rate = func.get_FX_exchange_rate("KRW","USD", rate_dezimal_too_long=True)
    DB_func.write_FX_rate(dict_FX_rate)

""" Calculate USD prices based on the latest FX-exchange rates """
def step_3():
    for candle in dict_1min_candles_org:
        dict_1min_candles_in_USD.append(func.recalc_price_in_USD(candle))

    print(dict_1min_candles_in_USD)

""" Calculate the average price and the vwap for the min (price*volume) """
def step_4():
    for candle in dict_1min_candles_org:
        dict_1min_candles.append(func.calc_avg_price_and_vwap1min(candle))

    print(dict_1min_candles)



""" Main """
if __name__ == "__main__":

    #step_0()
    step_1()
    # step_2()
    step_3()