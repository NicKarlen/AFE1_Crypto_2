import sqlite3


"""
    Create tables for the DB
"""
# Create a table for the FX_rates
def create_fx_rate_table():
    # Documentation can be found here: https://docs.python.org/3/library/sqlite3.html
    # Connect to database 'database.db' or create one if it doesn't exist.
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""CREATE TABLE FX_rates (
        tradingpair TEXT,
        timestamp TEXT,
        base TEXT,
        quote TEXT,
        rate_baseToQuote REAL
        )""")

    # DATATYPE for sqlite = NULL, INTEGER, REAL, TEXT, BLOB

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Create a table for the One_min_candles
def create_1min_candle_table():
    # Documentation can be found here: https://docs.python.org/3/library/sqlite3.html
    # Connect to database 'database.db' or create one if it doesn't exist.
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""CREATE TABLE One_Min_Candles (
        tradingpair TEXT,
        timestamp TEXT,
        exchange TEXT,
        price_low REAL,
        price_high REAL,
        price_close REAL,
        volume REAL,
        FX_rate REAL,
        price_low_USD REAL,
        price_high_USD REAL,
        price_close_USD REAL,
        avg_price_USD REAL,
        VWAP_1min REAL
        )""")

    # DATATYPE for sqlite = NULL, INTEGER, REAL, TEXT, BLOB

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Create a table for the VWAP1h
def create_VWAP1h():
    # Connect to database 'database.db' or create one if it doesn't exist.
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""CREATE TABLE Moving_avg_VWAP1h (
        tradingpair TEXT,
        timestamp TEXT,
        exchange TEXT,
        moving_avg_VWAP1h REAL,
        timestamp_from TEXT,
        timestamp_to TEXT
        )""")

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Create a table for the arbitrage Index
def create_Arb_idx():
    # Connect to database 'database.db' or create one if it doesn't exist.
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""CREATE TABLE Arbitrage_Index (
        commen_currency TEXT,
        timestamp TEXT,
        exchanges TEXT,
        VWAP_1h_min REAL,
        VWAP_1h_max REAL,
        arbitrage_index REAL
        )""")

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()


"""
    Write in tables on the DB
"""
# Write the FX rates in the DB
def write_FX_rate(dict_FX_rate):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    new_values = [(dict_FX_rate["tradingpair"], dict_FX_rate["timestamp"],
               dict_FX_rate["base"], dict_FX_rate["quote"], dict_FX_rate["rate_base_to_quote"])]

    cursor.executemany(
        "INSERT INTO FX_rates VALUES (?,?,?,?,?)", new_values)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Write the 1min candles in the DB
def write_1min_candle_table(dict_1min_candles):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    new_values = [(dict_1min_candles["tradingpair"],
               dict_1min_candles["timestamp"],
               dict_1min_candles["exchange"],
               dict_1min_candles["price_low"],
               dict_1min_candles["price_high"],
               dict_1min_candles["price_close"],
               dict_1min_candles["volume"],
               dict_1min_candles["FX_rate"],
               dict_1min_candles["price_low_USD"],
               dict_1min_candles["price_high_USD"],
               dict_1min_candles["price_close_USD"],
               dict_1min_candles["avg_price_USD"],
               dict_1min_candles["VWAP_1min"]
               )]

    cursor.executemany(
        "INSERT INTO One_Min_Candles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", new_values)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Write the VWAP1h in the DB
def write_VWAP1h(dict_VWAP1h):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    new_values = [(dict_VWAP1h["tradingpair"],
               dict_VWAP1h["timestamp"],
               dict_VWAP1h["exchange"],
               dict_VWAP1h["moving_avg_VWAP1h"],
               dict_VWAP1h["timestamp_from"],
               dict_VWAP1h["timestamp_to"]
               )]

    cursor.executemany(
        "INSERT INTO Moving_avg_VWAP1h VALUES (?,?,?,?,?,?)", new_values)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Write the Arbitrage Index in the DB
def write_arb_idx(dict_arb_idx):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    new_values = [(dict_arb_idx["commen_currency"],
               dict_arb_idx["timestamp"],
               dict_arb_idx["exchanges"],
               dict_arb_idx["VWAP_1h_min"],
               dict_arb_idx["VWAP_1h_max"],
               dict_arb_idx["arbitrage_index"]
               )]

    cursor.executemany(
        "INSERT INTO Arbitrage_Index VALUES (?,?,?,?,?,?)", new_values)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()


"""
    Read in tables on the DB
"""
# Read the latest FX rate for a cirtain tradingpair
def read_FX_rate(FX_pair):
    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create query string
    # Get rate_baseToQuote row where the tradingpair = the "FX_pair" then order it by timestamp and put it in descending order and only give back the first value
    query = f"SELECT rate_baseToQuote FROM FX_rates WHERE tradingpair LIKE '{FX_pair}' ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(query)

    # fetch it from the db and print it to the console
    res = list(cursor.fetchone())

    # Close our connection
    conn.close()

    return res

# Read candles for exchange X from the last 60min.
def read_One_Min_Candles(tradingpair):
    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create query string
    query = f"SELECT tradingpair, timestamp, exchange, volume, avg_price_USD, VWAP_1min FROM One_Min_Candles WHERE tradingpair LIKE '{tradingpair}' ORDER BY timestamp DESC LIMIT 60"
    cursor.execute(query)

    # fetch it from the db and print it to the console
    res = cursor.fetchall()

    # Close our connection
    conn.close()

    return res

# Read Moving_avg_VWAP1h from the last minute from all 3 exchanges.
def read_Moving_avg_VWAP1h(base):
    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # Create query string
    query = f"SELECT * FROM Moving_avg_VWAP1h WHERE tradingpair LIKE '%{base}%' ORDER BY timestamp DESC LIMIT 3"
    cursor.execute(query)

    # fetch it from the db and print it to the console
    res = cursor.fetchall()

    # Close our connection
    conn.close()

    return res