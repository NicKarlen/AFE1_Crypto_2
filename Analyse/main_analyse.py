from turtle import color
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# Insert the DB name which is stored in the forlder Analyse/DB
db_name = "database_26042022_bis_08052022.db"

# Create a connection to the database
con = sqlite3.connect(f"Analyse/DB/{db_name}")

# read the table of the arbitrage index
df_arb = pd.read_sql_query("SELECT timestamp, arbitrage_index FROM Arbitrage_Index", con)
df_Upbit = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE exchange LIKE 'Upbit' ORDER BY timestamp", con)
df_Coinbase = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE exchange LIKE 'Coinbase' ORDER BY timestamp", con)
df_Bitstamp = pd.read_sql_query("SELECT timestamp, volume, avg_price_USD FROM One_Min_Candles WHERE exchange LIKE 'Bitstamp' ORDER BY timestamp", con)

# Close our connection
con.close()

# merge the volume of the tree exchanges to the df
df = pd.merge(df_arb,df_Upbit, on=['timestamp'])
df.rename(columns={'volume': 'vol_Upbit', "avg_price_USD": "avg_price_USD_Upbit"}, inplace=True)

df = pd.merge(df,df_Coinbase, on=['timestamp'])
df.rename(columns={'volume': 'vol_Coinbase', "avg_price_USD": "avg_price_USD_Coinbase"}, inplace=True)

df = pd.merge(df,df_Bitstamp, on=['timestamp'])
df.rename(columns={'volume': 'vol_Bitstamp', "avg_price_USD": "avg_price_USD_Bitstamp"}, inplace=True)


# Create a plot-window with tree seperate plots with a shared X axis
fig, axes = plt.subplots(nrows=4, sharex=True)

# Output a plot of the arbitrage index with the volume of Upbit behind
df.plot(kind="line",x="timestamp", y=["vol_Upbit", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[0], grid=True)

axes[0].set_ylabel('Volumen in BTC')
axes[0].right_ax.set_ylabel('Arbitrage Index')
axes[0].get_legend().set_bbox_to_anchor((0.12, 1))

# Output a plot of the arbitrage index with the volume of Coinbace behind
df.plot(kind="line",x="timestamp", y=["vol_Coinbase", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[1], grid=True)

axes[1].set_ylabel('Volumen in BTC')
axes[1].right_ax.set_ylabel('Arbitrage Index')
axes[1].get_legend().set_bbox_to_anchor((0.12, 1))

# Output a plot of the arbitrage index with the volume of Bitstamp behind
df.plot(kind="line",x="timestamp", y=["vol_Bitstamp", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[2], grid=True)

axes[2].set_ylabel('Volumen in BTC')
axes[2].right_ax.set_ylabel('Arbitrage Index')
axes[2].get_legend().set_bbox_to_anchor((0.12, 1))

# Output a plot of the avg prices on exchanges
df.plot(kind="line",x="timestamp", y=["avg_price_USD_Upbit", "avg_price_USD_Coinbase", "avg_price_USD_Bitstamp"],
        color=["blue", "black", "green"], secondary_y=["arbitrage_index"], ax=axes[3], grid=True)

axes[3].set_ylabel('Preis in USD')
axes[3].set_xlabel('Zeitstempel')


plt.show()


