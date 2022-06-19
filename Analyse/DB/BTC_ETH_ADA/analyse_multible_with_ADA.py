from turtle import color
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# Insert the DB name which is stored in the forlder Analyse/DB
db_name = 'database_08062022_bis_16062022.db'  # "database_bis_08062022.db" # 

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

# arb index von ADA korrigieren
def check_arb_index(row):
    if row['arbitrage_index'] > 1.2:
        row['arbitrage_index'] = 1.0
    return row
df_arb_ADA = df_arb_ADA.apply(check_arb_index, axis='columns')

# Create two dataframes with the combined volume of BTC and ETH
df_vol_BTC = df_KRW_BTC.loc[:,['timestamp', 'volume']].copy()
df_vol_BTC = pd.merge(df_vol_BTC,df_BTC_USD[['timestamp', 'volume']], on=['timestamp'])
df_vol_BTC = pd.merge(df_vol_BTC,df_BTC_EUR[['timestamp', 'volume']], on=['timestamp'])
df_vol_BTC['Sum_Volume'] = df_vol_BTC['volume_x'] + df_vol_BTC['volume_y'] + df_vol_BTC['volume']

# Create two dataframes with the combined volume of BTC and ETH
df_vol_ETH = df_KRW_ETH.loc[:,['timestamp', 'volume']].copy()
df_vol_ETH = pd.merge(df_vol_ETH,df_ETH_USD[['timestamp', 'volume']], on=['timestamp'])
df_vol_ETH = pd.merge(df_vol_ETH,df_ETH_EUR[['timestamp', 'volume']], on=['timestamp'])
df_vol_ETH['Sum_Volume'] = df_vol_ETH['volume_x'] + df_vol_ETH['volume_y'] + df_vol_ETH['volume']

# Create a plot-window with tree seperate plots with a shared X axis
fig, axes = plt.subplots(nrows=4, sharex=True)

# Output a plot of the arbitrage index
df_arb_BTC.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["red"], ax=axes[0], grid=True)
df_arb_ETH.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["blue"], ax=axes[0], grid=True)
df_arb_ADA.plot(kind="line",x="timestamp", y=["arbitrage_index"], color=["black"], ax=axes[0], grid=True)

axes[0].set_ylabel('Arbitrage Index')
axes[0].legend(labels=['Arbitrage Index von Bitcoin (BTC)', 'Arbitrage Index von Ethereum (ETH)', 'Arbitrage Index von Cardano (ADA)']) 

# Output a plot of the avg prices & arbIndex on exchanges BTC
#df_arb_BTC.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[1], grid=True)
df_KRW_BTC.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[1], grid=True)
df_BTC_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[1], grid=True)
df_BTC_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[1], grid=True)
#df_vol_BTC.plot(kind="line",x="timestamp", y=["Sum_Volume"], color=["lightblue"], secondary_y=["Sum_Volume"], ax=axes[1], grid=True)


# Output a plot of the avg prices on exchanges ETH
#df_arb_ETH.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[2], grid=True)
df_KRW_ETH.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[2], grid=True)
df_ETH_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[2], grid=True)
df_ETH_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[2], grid=True)
#df_vol_ETH.plot(kind="line",x="timestamp", y=["Sum_Volume"], color=["lightblue"], secondary_y=["Sum_Volume"], ax=axes[2], grid=True)

# Output a plot of the avg prices on exchanges ADA
# #df_arb_ADA.plot(kind="line",x="timestamp", y=["arbitrage_index"], secondary_y=["arbitrage_index"], color=["red"], ax=axes[3], grid=True)
df_KRW_ADA.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["blue"], ax=axes[3], grid=True)
df_ADA_USD.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["black"], ax=axes[3], grid=True)
df_ADA_EUR.plot(kind="line",x="timestamp", y=["avg_price_USD"], color=["green"], ax=axes[3], grid=True)

# lines, labels = axes[1].get_legend_handles_labels()
# lines1, labels1 = axes[1].right_ax.get_legend_handles_labels()
# axes[1].legend(lines+lines1, ['BTC Preis von Upbit', 'BTC Preis von Coinbase', 'BTC Preis von Bitstamp', 'Summe der Volumen in BTC'], loc=0)
# axes[1].right_ax.set_ylabel('Volumen in BTC')

axes[1].legend(['BTC Preis von Upbit', 'BTC Preis von Coinbase', 'BTC Preis von Bitstamp'])
axes[1].set_ylabel('Preis in USD')
axes[1].set_xlabel('Zeitstempel')



# lines, labels = axes[2].get_legend_handles_labels()
# lines1, labels1 = axes[2].right_ax.get_legend_handles_labels()
# axes[2].legend(lines+lines1, ['ETH Preis von Upbit', 'ETH Preis von Coinbase', 'ETH Preis von Bitstamp', 'Summe der Volumen in ETH'], loc=0)
# axes[2].right_ax.set_ylabel('Volumen in ETH')

axes[2].legend(['ETH Preis von Upbit', 'ETH Preis von Coinbase', 'ETH Preis von Bitstamp'])
axes[2].set_ylabel('Preis in USD')
axes[2].set_xlabel('Zeitstempel')


axes[3].set_ylabel('Preis in USD')
axes[3].set_xlabel('Zeitstempel')
axes[3].legend(labels=['Preis von Upbit', 'Preis von Coinbase', 'Preis von Bitstamp'])
# #axes[3].right_ax.set_ylabel('Arbitrage Index')

# Set titel
fig.suptitle("Arbitrage Index für Bitcoin, Ethereum und Cardano an den Börsen Coinbase, Bitstamp und Upbit (08.06.22 19:32 - 16.06.22 06:31)")


plt.show()


