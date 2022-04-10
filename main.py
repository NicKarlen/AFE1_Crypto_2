from upbit.client import Upbit


"""
    Upbit client do get the 1 minute candle for the tradingpair KRW-BTC
"""
client = Upbit()
resp = client.Candle.Candle_minutes(
    unit=1, # 1-min. candle
    market='KRW-BTC', #Traingpair
    count= 1   # 60 candles
    #to="2022-04-10 16:00:00"  #yyyy-MM-dd HH:mm:ss
)
print(resp['result'])