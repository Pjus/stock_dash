from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from pandas_datareader import data as pdr

from analysis.get_indicators import BBANDS, rsi, mfi, atr, ForceIndex, EMV

import yfinance as yf
import pandas as pd
import json

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')


def macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df


def get_macd(request, ticker, day):
    stock_price = pdr.get_data_yahoo(ticker)

    results = stock_price['Adj Close'].ewm(span = day, adjust = False).mean()
    results_json = results.to_json()
    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")


def get_BBAND(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)
    results = BBANDS(stock_price, 50)
    results = results[['MiddleBand', 'UpperBand', 'LowerBand']]
    results_json = results.to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")


def get_RSI(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)

    # Call RSI function from the talib library to calculate RSI
    stock_price['RSI'] = rsi(stock_price['Adj Close'])
    results = stock_price[['RSI']]
    results_json = results.to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")


def get_MFI(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)
    
    stock_price['MFI'] = mfi(stock_price['High'], stock_price['Low'], stock_price['Close'], stock_price['Volume'], 14)

    results = stock_price[['MFI']]
    results_json = results.to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")



def get_ATR(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)

    stock_price['ATR'] = atr(stock_price['High'], stock_price['Low'], stock_price['Close'], 14)

    results = stock_price[['ATR']]
    results_json = results.to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")


def get_Force_Index(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)

    n = 1
    stock_ForceIndex = ForceIndex(stock_price, n)
    results_json = stock_ForceIndex[['ForceIndex']].to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")


def get_EMV(request, ticker):
    stock_price = pdr.get_data_yahoo(ticker)

    # Compute the 14-day Ease of Movement for AAPL
    n = 14
    stock_EMV = EMV(stock_price, n)
    results = stock_EMV['EMV']
    results_json = results.to_json()

    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")




