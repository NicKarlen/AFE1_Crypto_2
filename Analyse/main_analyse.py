from turtle import color
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# Insert the DB name which is stored in the forlder Analyse/DB
db_name = "database_20042022_bis_24042022.db"

# Create a connection to the database
con = sqlite3.connect(f"Analyse/DB/{db_name}")

# read the table of the arbitrage index
df_arb = pd.read_sql_query("SELECT timestamp, arbitrage_index FROM Arbitrage_Index", con)
df_vol_Upbit = pd.read_sql_query("SELECT timestamp, volume FROM One_Min_Candles WHERE exchange LIKE 'Upbit' ORDER BY timestamp", con)
df_vol_Coinbase = pd.read_sql_query("SELECT timestamp, volume FROM One_Min_Candles WHERE exchange LIKE 'Coinbase' ORDER BY timestamp", con)
df_vol_Bitstamp = pd.read_sql_query("SELECT timestamp, volume FROM One_Min_Candles WHERE exchange LIKE 'Bitstamp' ORDER BY timestamp", con)

# Close our connection
con.close()

# merge the volume of the tree exchanges to the df
df = pd.merge(df_arb,df_vol_Upbit, on=['timestamp'])
df.rename(columns={'volume': 'vol_Upbit'}, inplace=True)

df = pd.merge(df,df_vol_Coinbase, on=['timestamp'])
df.rename(columns={'volume': 'vol_Coinbase'}, inplace=True)

df = pd.merge(df,df_vol_Bitstamp, on=['timestamp'])
df.rename(columns={'volume': 'vol_Bitstamp'}, inplace=True)


# Create a plot-window with tree seperate plots with a shared X axis
fig, axes = plt.subplots(nrows=3, sharex=True)

# Output a plot of the arbitrage index with the volume of Upbit behind
df.plot(kind="line",x="timestamp", y=["vol_Upbit", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[0])
# plt.show()


# Output a plot of the arbitrage index with the volume of Coinbace behind
df.plot(kind="line",x="timestamp", y=["vol_Coinbase", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[1])
# plt.show()

# Output a plot of the arbitrage index with the volume of Bitstamp behind
df.plot(kind="line",x="timestamp", y=["vol_Bitstamp", "arbitrage_index"],
        color=["lightblue", "red"], secondary_y=["arbitrage_index"], ax=axes[2])
plt.show()


