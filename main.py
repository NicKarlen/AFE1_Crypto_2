from datetime import datetime, timedelta
from time import sleep
import func
import DB_func
import time
import logging

""" Global variables """
dict_1min_candles = []
arr_Upbit_tradingpairs = ['KRW-BTC', 'KRW-ETH', 'KRW-ADA']
arr_Coinbase_tradingpairs = ['BTC-USD', 'ETH-USD', 'ADA-USD']
arr_Bitstamp_tradingpairs = ['btceur', 'etheur', 'adaeur']

""" Create database """
def step_0():
    # DB_func.create_fx_rate_table()
    # DB_func.create_1min_candle_table()
    # DB_func.create_VWAP1h()
    DB_func.create_Arb_idx()

""" Get 1 min candle from the exchanges """
def step_1():
    # IDEA: We cound put each exchange request in try except and return the same response we got 1 min ago if the request fails.
    #       Safe the dict from one min ago and everytime we end the function we override the "old" dict with the new one.
    #       I think this would have minimal impact on the analysis we are going to do.

    dict_1min_candles_org = []
    for tradingpair in arr_Upbit_tradingpairs:
        dict_1min_candles_org.append(func.get_1min_Upbit(tradingpair))
    for tradingpair in arr_Coinbase_tradingpairs:
        dict_1min_candles_org.append(func.get_1min_Coinbase(tradingpair))
    for tradingpair in arr_Bitstamp_tradingpairs:
        dict_1min_candles_org.append(func.get_1min_Bitstamp(tradingpair))

    # print
    # for i in range(12):
    #     print(dict_1min_candles_org[i])


    return dict_1min_candles_org


""" Get the exchange rate for the FX pairs needed (EUR-USD & KRW-USD) """
def step_2():

    #dict_FX_rate = func.get_FX_exchange_rate_old("EUR","USD", rate_dezimal_too_long=False)
    dict_FX_rate = func.get_FX_exchange_rate_new("EUR","USD")
    DB_func.write_FX_rate(dict_FX_rate)

    #dict_FX_rate = func.get_FX_exchange_rate_old("KRW","USD", rate_dezimal_too_long=True)
    dict_FX_rate = func.get_FX_exchange_rate_new("KRW","USD")
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

        # dict_1min_candles.append(dict_1min_candle)

""" Calc moving avg. VWAP_1h """
def step_5():
    for pair in ['KRW-BTC', 'KRW-ETH', 'KRW-ADA']:
        DB_func.write_VWAP1h(func.calc_VWAP_1h(pair))
    for pair in ['BTC-USD', 'ETH-USD', 'ADA-USD']:
        DB_func.write_VWAP1h(func.calc_VWAP_1h(pair))
    for pair in ['BTC-EUR', 'ETH-EUR', 'ADA-EUR']:
        DB_func.write_VWAP1h(func.calc_VWAP_1h(pair))

""" Calc arbitrage index based on the moving avg. VWAP_1h """
def step_6():
    for base in ['BTC', 'ETH', 'ADA']:
        DB_func.write_arb_idx(func.calc_arb_idx(base))

""" RUN modes """    
def auto_run():
    time_start = datetime.utcnow()
    count_minutes = 0
    while True:
        time_now = datetime.utcnow()
        if time_now.minute > 5 and count_minutes > 59:
            count_minutes = 0
            try:
                step_2() # Only call every hour (max calls 100/day)
            except:
                time.sleep(10)
                logging.warning("**************** API calls to FX-endpoint failed the first time ********************")
                step_2() # Only call every hour (max calls 100/day)
            
            logging.info("Timestamp: %s   FX-Rates updated", time_now)

        if time_now.second > 30:
            try:
                dict_1min_candles_org = step_1()
            except:
                time.sleep(10)
                logging.warning("**************** API calls to the exchanges failed the first time ********************")
                dict_1min_candles_org = step_1()
                    

            dict_1min_candles_in_USD = step_3(dict_1min_candles_org)
            step_4(dict_1min_candles_in_USD)

            # wait for 65 min until we have enough recorded 1min candles
            if time_start + timedelta(minutes=65) < time_now:
                step_5()
                step_6()

            count_minutes += 1
            logging.info("Timestamp: %s   Count Minutes: %s", time_now, count_minutes)
            print(time_now, "   Count Minutes: ", count_minutes)
            time.sleep(30)

def manual_run():
    # step_0()
    # dict_1min_candles_org = step_1()
    step_2() # Only call every hour (max calls 100/day)
    # dict_1min_candles_in_USD = step_3(dict_1min_candles_org)
    # for i in range(12):
    #     print(dict_1min_candles_in_USD[i])
    # step_4(dict_1min_candles_in_USD)
    # step_5()
    # step_6()


""" Main """
if __name__ == "__main__":
    print("Code running..........", datetime.now())
    # initialyse logger
    logging.basicConfig(filename='ArbitrageIndex.log', encoding='utf-8', level=logging.INFO)
    logging.info("Started logging,  Code running..........  %s", datetime.now())

    auto_run()

    # while True:
    #     time_now = datetime.utcnow()

    #     if time_now.second > 30:
    #         manual_run()
    #         time.sleep(30)

    print("Code finished.........", datetime.now())