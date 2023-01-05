from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from analysis.modules import get_collection
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
    price_collection = get_collection('stock_price')
    stock_price = price_collection.find_one({'ticker':ticker})['price']
    stock_price = pd.DataFrame(stock_price).T

    # results = macd(stock_price['Adj Close'], 26, 12, 9)

    results = stock_price['Adj Close'].ewm(span = day, adjust = False).mean()
    results_json = results.to_json()
    content = {
        "result":results_json,
    }

    return JsonResponse(content, content_type="application/json")

