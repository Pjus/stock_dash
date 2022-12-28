from datetime import datetime, timedelta, time
from django.shortcuts import render
from pymongo import MongoClient
from analysis.modules import get_price, get_last_day, get_currency, time_in_range, get_calender, get_collection, get_finviz_news
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
calender_collection = db['calender']



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

    nasdaq_last_day = get_last_day(nasdaq)
    dow_last_day = get_last_day(dow)
    snp_last_day = get_last_day(snp)


    if time_in_range(start, end, now.time()):
        get_price(nasdaq, yesterday)
        get_price(dow, yesterday)
        get_price(snp, yesterday)
        get_currency()
        get_calender()

    nas_price = price_collection.find_one({'ticker':nasdaq})['price']
    dow_price = price_collection.find_one({'ticker':dow})['price']
    snp_price = price_collection.find_one({'ticker':snp})['price']
    try:
        currency = currency_collection.find_one({'date':today})['currency']
    except:
        get_currency()
        currency = currency_collection.find_one({'date':today})['currency']
 
    calender = calender_collection.find_one()
    if calender == None:
        get_calender()
        calender = calender_collection.find_one()
    nas_df = pd.DataFrame(nas_price).T.pct_change()
    dow_df = pd.DataFrame(dow_price).T.pct_change()
    snp_df = pd.DataFrame(snp_price).T.pct_change()

    krw = currency

    news_collection = get_collection("news")
    fin_news = news_collection.find_one({'press':"fin"})['news']


    context = {
        "nasdaq": round(nas_price[nasdaq_last_day]['Adj Close'], 2),
        "dow":round(dow_price[dow_last_day]['Adj Close'], 2),
        "snp":round(snp_price[snp_last_day]['Adj Close'], 2),

        "nas_pct": round(nas_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "dow_pct": round(dow_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "snp_pct": round(snp_df.iloc[-1:, 3:4].values[0][0] * 100, 2),

        "currency": round(krw[today]['USD']['current'], 2),
        "currency_pct": krw[today]['USD']['change'],
        "calender": calender['calender'],

        "news": pd.DataFrame(fin_news).T[:30]

    }

    if request.user.is_authenticated:
        portfolio = Portfolio.objects.filter(author=request.user)
        context["portfolio"] = portfolio
        context["percent"] = 100
        total_account = 0
        for port in portfolio:
            total_account += port.port_value
        
        context['total_account'] = total_account
        return render(request, 'main/core.html', context)

    return render(request, 'main/core2.html', context)


def get_portable(request):
    portfolio = Portfolio.objects.filter(author=request.user)
    context = {"page":"Portfolio"}
    context["portfolio"] = portfolio
    return render(request, 'main/port_list.html', context)

def get_billing(request):
    return render(request, 'main/billing.html')

def get_box(request):
    return render(request, 'main/box.html')