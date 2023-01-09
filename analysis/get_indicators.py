# Load the necessary packages and modules
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Simple Moving Average 
def SMA(data, ndays): 
    SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = 'SMA') 
    data = data.join(SMA) 
    return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
    EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                 name = 'EWMA_' + str(ndays)) 
    data = data.join(EMA) 
    return data


def get_SMA(ticker, data):
    # Retrieve the Goolge stock data from Yahoo finance
    data = data
    close = data['Close']

    # Compute the 50-day SMA
    n = 50
    SMA = SMA(data,n)
    SMA = SMA.dropna()
    SMA = SMA['SMA']

    # Compute the 200-day EWMA
    ew = 200
    EWMA = EWMA(data,ew)
    EWMA = EWMA.dropna()
    EWMA = EWMA['EWMA_200']

    return EWMA

# Compute the Bollinger Bands 
def BBANDS(data, window=50):
    MA = data['Adj Close'].rolling(window=window).mean()
    SD = data['Adj Close'].rolling(window=window).std()
    data['MiddleBand'] = MA
    data['UpperBand'] = MA + (2 * SD) 
    data['LowerBand'] = MA - (2 * SD)

    return data
