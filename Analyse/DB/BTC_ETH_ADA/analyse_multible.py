from turtle import color
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# Insert the DB name which is stored in the forlder Analyse/DB
db_name = "database.db"

# Create a connection to the database
con = sqlite3.connect(f"Analyse/DB/BTC_ETH_ADA/{db_name}")

# read the table of the arbitrage index
df_arb_BTC = pd.read_sql_query("SELECT timestamp, arbitrage_index FROM Arbitrage_Index WHERE commen_currency LIKE 'BTC' ORDER BY timestamp", con)
df_arb_ETH = pd.read_sql_query("SELECT timestamp, arbitrage_index FROM Arbitrage_Index WHERE commen_currency LIKE 'ETH' ORDER BY timestamp", con)
df_arb_ADA = pd.read_sql_query("SELECT timestamp, arbitrage_index FROM Arbitrage_Index WHERE commen_currency LIKE 'ADA' ORDER BY timestamp", con)

df_KRW_BTC = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'KRW-BTC' ORDER BY timestamp", con)
df_KRW_ETH = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'KRW-ETH' ORDER BY timestamp", con)
df_KRW_ADA = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'KRW-ADA' ORDER BY timestamp", con)

df_BTC_USD = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'BTC-USD' ORDER BY timestamp", con)
df_ETH_USD = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'ETH-USD' ORDER BY timestamp", con)
df_ADA_USD = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'ADA-USD' ORDER BY timestamp", con)

df_BTC_EUR = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'BTC-EUR' ORDER BY timestamp", con)
df_ETH_EUR = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'ETH-EUR' ORDER BY timestamp", con)
df_ADA_EUR = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE tradingpair LIKE 'ADA-EUR' ORDER BY timestamp", con)

# Close our connection
con.close()

# Create a plot-window with tree seperate plots with a shared X axis
fig, axes = plt.subplots(nrows=4, sharex=True)

# Output a plot of the arbitrage index
df_arb_BTC.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["red"], ax=axes[0], grid=True)
df_arb_ETH.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["blue"], ax=axes[0], grid=True)
df_arb_ADA.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["black"], ax=axes[0], grid=True)

axes[0].set_ylabel('Arbitrage Index')

# Output a plot of the avg prices & arbIndex on exchanges BTC
#df_arb_BTC.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[1], grid=True)
df_KRW_BTC.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[1], grid=True)
df_BTC_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[1], grid=True)
df_BTC_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[1], grid=True)

# Output a plot of the avg prices on exchanges ETH
#df_arb_ETH.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[2], grid=True)
df_KRW_ETH.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[2], grid=True)
df_ETH_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[2], grid=True)
df_ETH_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[2], grid=True)

# Output a plot of the avg prices on exchanges ADA
#df_arb_ADA.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[3], grid=True)
df_KRW_ADA.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[3], grid=True)
df_ADA_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[3], grid=True)
df_ADA_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[3], grid=True)

axes[1].set_ylabel('Preis in USD')
axes[1].set_xlabel('Zeitstempel')
#axes[1].right_ax.set_ylabel('Arbitrage Index')

axes[2].set_ylabel('Preis in USD')
axes[2].set_xlabel('Zeitstempel')
#axes[2].right_ax.set_ylabel('Arbitrage Index')

axes[3].set_ylabel('Preis in USD')
axes[3].set_xlabel('Zeitstempel')
#axes[3].right_ax.set_ylabel('Arbitrage Index')


plt.show()


