from datetime import datetime, timedelta, time
from django.shortcuts import render
from pymongo import MongoClient
from analysis.modules import get_price, get_last_day, get_currency, time_in_range, get_calender, get_collection, get_finviz_news
from portfolio.models import Portfolio

import yfinance as yf
import pandas as pd
import json
import re
from pandas_datareader import data as pdr

yf.pdr_override()

TODAY_DOWN = False

yf.pdr_override()
with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)


client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']

price_collection = db['stock_price']
currency_collection = db['currency']
calender_collection = db['calender']



yesterday_origin = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday_origin, '%Y-%m-%d')

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

    print(yesterday)
    print(nasdaq_last_day)

    if time_in_range(start, end, now.time()):
        get_price(nasdaq, yesterday)
        get_price(dow, yesterday)
        get_price(snp, yesterday)
        get_currency()
        get_calender()
    
    # try:
    #     price_collection.find_one({'ticker':nasdaq})['price'][yesterday]
    #     price_collection.find_one({'ticker':dow})['price'][yesterday]
    #     price_collection.find_one({'ticker':snp})['price'][yesterday]

    #     nas_price = price_collection.find_one({'ticker':nasdaq})['price']
    #     dow_price = price_collection.find_one({'ticker':dow})['price']
    #     snp_price = price_collection.find_one({'ticker':snp})['price']
    # except:
    #     get_price(nasdaq, yesterday)
    #     get_price(dow, yesterday)
    #     get_price(snp, yesterday)
        
    #     nas_price = price_collection.find_one({'ticker':nasdaq})['price']
    #     dow_price = price_collection.find_one({'ticker':dow})['price']
    #     snp_price = price_collection.find_one({'ticker':snp})['price']
    


    try:
        currency = currency_collection.find_one({'date':today})['currency']
    except:
        get_currency()
        currency = currency_collection.find_one({'date':today})['currency']
 
    calender = calender_collection.find_one({'date':today})
    if calender == None:
        get_calender()
        calender = calender_collection.find_one()


    nas_df = pdr.get_data_yahoo(nasdaq)
    dow_df = pdr.get_data_yahoo(dow)
    snp_df = pdr.get_data_yahoo(snp)

    nas_diff = nas_df.diff()
    dow_diff = dow_df.diff()
    snp_diff = snp_df.diff()

    nas_pct = nas_df.pct_change()
    dow_pct = dow_df.pct_change()
    snp_pct = snp_df.pct_change()

    print(nas_pct)

    krw = currency

    news_collection = get_collection("news")
    fin_news = news_collection.find_one({'press':"fin"})['news']
    
    day_defore = krw[today]['USD']['day_before']


    context = {
        "nasdaq": round(nas_df.iloc[-1:,4], 2)[0],
        "dow":round(dow_df.iloc[-1:,4], 2)[0],
        "snp":round(snp_df.iloc[-1:,4], 2)[0],

        "nas_pct": round(nas_pct.iloc[-1:, 4][0] * 100, 2),
        "dow_pct": round(dow_pct.iloc[-1:, 4][0] * 100, 2),
        "snp_pct": round(snp_pct.iloc[-1:, 4][0] * 100, 2),

        "nas_diff": round(nas_diff.iloc[-1:, 3:4].values[0][0], 2),
        "dow_diff": round(dow_diff.iloc[-1:, 3:4].values[0][0], 2),
        "snp_diff": round(snp_diff.iloc[-1:, 3:4].values[0][0], 2),

        "currency": round(krw[today]['USD']['current'], 2),
        "currency_chg": float(day_defore),
        "currency_pct": krw[today]['USD']['change'],
        "calender": calender['calender'],

        "news": pd.DataFrame(fin_news).T[:30]

    }

    if request.user.is_authenticated:
        portfolio = Portfolio.objects.filter(author=request.user)
        context["portfolio"] = portfolio
        curr_month_return = 0
        prev_month_return = 0
        prev_month = ''
        curr_month = ''

        total_account = 0
        monthly_returns = {}
        port_history = {}

        for port in portfolio:
            for stock in port.stock_port.all():
                temp = json.loads(stock.profit_history)
                for key, value in temp.items():
                    if key in monthly_returns:
                        monthly_returns[key] += value['profit']
                    else:
                        monthly_returns[key] = value['profit']

            total_account += port.port_value
            if total_account != 0:
                for idx, port in enumerate(portfolio):
                    port.weight = round((port.port_value / total_account) * 100, 2)
            else:
                port.weight = 0
                port.save()

            temp_history = json.loads(port.port_history)

            for key, value in temp_history.items():
                if key in port_history:
                    port_history[key] += value
                else:
                    port_history[key] = value

        print(port_history)
        context['total_account'] = total_account
        context['monthly_returns'] = json.dumps(monthly_returns) 
        context['port_history'] = json.dumps(port_history) 


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