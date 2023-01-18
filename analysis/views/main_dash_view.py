from datetime import datetime, timedelta, time
from django.shortcuts import render
from django.db.models import Q

from analysis.modules import get_calender, get_finviz_news, get_sec_news, get_currency, get_price, get_index
from portfolio.models import Portfolio

import yfinance as yf
import pandas as pd
import json
import re
from pandas_datareader import data as pdr

from ..models import FinEventDate, FinancialEvent, FinNews, Currency, StockCompany, CompanyPrice

yf.pdr_override()

TODAY_DOWN = False

yf.pdr_override()


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
    context = {}

    # Nasdaq  
    stock = StockCompany.objects.filter(Q(ticker=nasdaq))
    price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    if len(price_list) == 0:
        get_index(nasdaq)
        price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    df = pd.DataFrame(list(price_list.values()))
    df = df[['adj_close_price']]

    context['nas_diff'] = round(df.diff().iloc[-1:,:].values[0][0], 2) 
    context['nas_pct'] = round(df.pct_change().iloc[-1:,:].values[0][0] * 100, 2)
    context['nasdaq'] = round(price_list[len(price_list)-1].close_price, 2) 

    # Snp
    stock = StockCompany.objects.filter(Q(ticker=snp))
    price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    if len(price_list) == 0:
        get_index(snp)
        price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    df = pd.DataFrame(list(price_list.values()))
    df = df[['adj_close_price']]

    context['snp_diff'] = round(df.diff().iloc[-1:,:].values[0][0], 2) 
    context['snp_pct'] = round(df.pct_change().iloc[-1:,:].values[0][0] * 100, 2)
    context['snp'] = round(price_list[len(price_list)-1].close_price, 2) 

    # Dow
    stock = StockCompany.objects.filter(Q(ticker=dow))
    price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    if len(price_list) == 0:
        get_index(dow)
        price_list = CompanyPrice.objects.filter(Q(ticker=stock[0]))

    df = pd.DataFrame(list(price_list.values()))
    df = df[['adj_close_price']]

    context['dow_diff'] = round(df.diff().iloc[-1:,:].values[0][0], 2) 
    context['dow_pct'] = round(df.pct_change().iloc[-1:,:].values[0][0] * 100, 2)
    context['dow'] = round(price_list[len(price_list)-1].close_price, 2) 


    # Events
    event_list = FinEventDate.objects.order_by('fin_current_date')
    if len(event_list) == 0:
        get_calender()
        event_detail = FinancialEvent.objects.order_by('event_mother')
        context['event_detail_list'] = event_detail[:11]
    else:
        event_detail = FinancialEvent.objects.order_by('event_mother')
        context['event_detail_list'] = event_detail[:11]

    # News
    news_list = FinNews.objects.order_by('date')
    if len(event_list) == 0:
        get_finviz_news()
        sec_news_list = news_list.filter(Q(press="fin")).distinct()
        context['news_list'] = sec_news_list[:21]
    else:
        sec_news_list = news_list.filter(Q(press="fin")).distinct()
        context['news_list'] = sec_news_list[:21]

    # Currency
    currency_list = Currency.objects.order_by('date')
    if len(currency_list) == 0:
        get_currency()
        currency_list = currency_list.filter(Q(country="USD")).distinct()
        context['currency'] = currency_list[len(currency_list)-1]
    else:
        currency_list = currency_list.filter(Q(country="USD")).distinct()
        context['currency'] = currency_list[len(currency_list)-1]


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