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
        price_low REAL,
        price_high REAL,
        price_close REAL,
        volume REAL,
        avg_price REAL,
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