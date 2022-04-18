import sqlite3

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

# Write the FX rates in the DB
def write_FX_rate(dict_FX_rate):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    trades = [(dict_FX_rate["tradingpair"], dict_FX_rate["timestamp"],
               dict_FX_rate["base"], dict_FX_rate["quote"], dict_FX_rate["rate_base_to_quote"])]

    cursor.executemany(
        "INSERT INTO FX_rates VALUES (?,?,?,?,?)", trades)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# Get the latest FX rate for a cirtain tradingpair
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

# Write the FX rates in the DB
def write_1min_candle_table(dict_1min_candles):

    # Connect to database 'database.db'
    conn = sqlite3.connect('data/database.db')

    # Create a cursor for db
    cursor = conn.cursor()

    # write a table to store in the database
    trades = [(dict_1min_candles["tradingpair"],
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
        "INSERT INTO One_Min_Candles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", trades)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()