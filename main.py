from datetime import datetime
from time import sleep
import func
import DB_func
import time

""" Global variables """
dict_1min_candles = []


""" Create database """
def step_0():
    # DB_func.create_fx_rate_table()
    # DB_func.create_1min_candle_table()
    DB_func.create_VWAP1h()

""" Get 1 min candle from the exchanges """
def step_1(): 
    dict_1min_candles_org = []
    dict_1min_candles_org.append(func.get_1min_Upbit("KRW-BTC"))
    dict_1min_candles_org.append(func.get_1min_Coinbase("BTC-USD"))
    dict_1min_candles_org.append(func.get_1min_Bitstamp("btceur"))
    # print(dict_1min_candles_org[0])
    # print(dict_1min_candles_org[1])
    # print(dict_1min_candles_org[2])
    return dict_1min_candles_org


""" Get the exchange rate for the FX pairs needed (EUR-USD & KRW-USD) """
def step_2():
    dict_FX_rate = func.get_FX_exchange_rate("EUR","USD", rate_dezimal_too_long=False)
    DB_func.write_FX_rate(dict_FX_rate)

    dict_FX_rate = func.get_FX_exchange_rate("KRW","USD", rate_dezimal_too_long=True)
    DB_func.write_FX_rate(dict_FX_rate)


""" Calculate USD prices based on the latest FX-exchange rates """
def step_3(dict_1min_candles_org):
    dict_1min_candles_in_USD = []
    for candle in dict_1min_candles_org:
        dict_1min_candles_in_USD.append(func.recalc_price_in_USD(candle))

    return dict_1min_candles_in_USD


""" Calculate the average price and the vwap for the min (price*volume) """
def step_4(dict_1min_candles_in_USD):
    for candle in dict_1min_candles_in_USD:

        dict_1min_candle = func.calc_avg_price_and_vwap1min(candle)
        DB_func.write_1min_candle_table(dict_1min_candle)

        dict_1min_candles.append(dict_1min_candle)

""" Calc moving avg. VWAP_1h """
def step_5():
    DB_func.write_VWAP1h(func.calc_VWAP_1h("KRW-BTC"))
    DB_func.write_VWAP1h(func.calc_VWAP_1h("BTC-USD"))
    DB_func.write_VWAP1h(func.calc_VWAP_1h("BTC-EUR"))


""" RUN modes """    
def auto_run():
    count_minutes = 0
    while True:
        time_now = datetime.utcnow()
        if time_now.minute > 5 and count_minutes > 59:
            count_minutes = 0
            step_2() # Only call every hour (max calls 100/day)
            print(time_now)

        if time_now.second > 30:
            dict_1min_candles_org = step_1()
            dict_1min_candles_in_USD = step_3(dict_1min_candles_org)
            step_4(dict_1min_candles_in_USD)
            step_5()
            count_minutes += 1
            print(time_now, count_minutes)
            time.sleep(30)

def manual_run():
    # step_0()
    # dict_1min_candles_org = step_1()
    # step_2() # Only call every hour (max calls 100/day)
    # dict_1min_candles_in_USD = step_3(dict_1min_candles_org)
    # step_4(dict_1min_candles_in_USD)
    step_5()


""" Main """
if __name__ == "__main__":
    print("Code running..........")

    # auto_run()

    manual_run()

    print("Code finished.........")