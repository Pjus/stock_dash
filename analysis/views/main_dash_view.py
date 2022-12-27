from datetime import datetime, timedelta, time
from django.shortcuts import render
from pymongo import MongoClient
from analysis.modules import get_price, get_last_day, get_currency, time_in_range
from portfolio.models import Portfolio

import yfinance as yf
import pandas as pd
import json

TODAY_DOWN = False

yf.pdr_override()
with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)


client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']

price_collection = db['stock_price']
currency_collection = db['currency']


yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')


start = time(7, 0, 0)
end = time(9, 0, 0)
now = datetime.now()

def board(request):
    nasdaq = "^IXIC"
    dow = "^DJI"
    snp = "^GSPC"
    if time_in_range(start, end, now.time()):
        get_price(nasdaq, yesterday)
        get_price(dow, yesterday)
        get_price(snp, yesterday)
        get_currency()

    nas_price = price_collection.find_one({'ticker':nasdaq})['price']
    dow_price = price_collection.find_one({'ticker':dow})['price']
    snp_price = price_collection.find_one({'ticker':snp})['price']

    currency = currency_collection.find_one({'date':today})['currency']

    nas_df = pd.DataFrame(nas_price).T.pct_change()
    dow_df = pd.DataFrame(dow_price).T.pct_change()
    snp_df = pd.DataFrame(snp_price).T.pct_change()

    krw = currency

    last_day = get_last_day(nasdaq)

    context = {
        "nasdaq": round(nas_price[last_day]['Adj Close'], 2),
        "dow":round(dow_price[last_day]['Adj Close'], 2),
        "snp":round(snp_price[last_day]['Adj Close'], 2),

        "nas_pct": round(nas_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "dow_pct": round(dow_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "snp_pct": round(snp_df.iloc[-1:, 3:4].values[0][0] * 100, 2),

        "currency": round(krw[today]['USD']['current'], 2),
        "currency_pct": krw[today]['USD']['change'],

    }
    if not request.user.is_authenticated:
        return render(request, 'main/core2.html', context)
    portfolio = Portfolio.objects.filter(author=request.user)
    context["portfolio"] = portfolio
    total_account = 0
    for port in portfolio:
        total_account += port.port_value
    return render(request, 'main/core.html', context)


def get_portable(request):
    portfolio = Portfolio.objects.filter(author=request.user)
    context = {"page":"Portfolio"}
    context["portfolio"] = portfolio
    return render(request, 'main/port_list.html', context)

def get_billing(request):
    return render(request, 'main/billing.html')

def get_box(request):
    return render(request, 'main/box.html')