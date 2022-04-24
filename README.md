# AFE1_Crypto_2
The goal of this code is to get price data from diffrent crypto exchanges and compare them to each other.

The whole project has three parts:

- Collect data
- Store data
- Analyse data

## 1.  Get Data

Here we use 3 exchanges to get the data from :
- Upbit
- Coinbase
- Bitstamp

From every exchange we get the 1 minute candle (from the past minute). 

The information we get is :
- timestamp
- price low
- price high
- price close
- volume

We then run some calculations to get the moving average of the VWAP (Volume weighted average price) over the past hour.

With that we calculate the so called **arbitrage index**. The **arbitrage index** is the ratio of the highest VWAP to the lowest VWAP over all exchanges.

## 2. Store data

All the data is stored in an sql database (with sqlite)


## 3. Analyse data

Not we analyse the date and check if there is any correlation between traded volume and the **arbitrage index**
