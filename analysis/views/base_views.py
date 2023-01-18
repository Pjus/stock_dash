from django.shortcuts import render
import yfinance as yf
import json
from datetime import datetime, timedelta

import pandas as pd
from pandas_datareader import data as pdr

import calendar


from tradingview_ta import TA_Handler, Interval, Exchange

yf.pdr_override()

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')

week_of_day = calendar.day_name[today_origin.weekday()]

# Create your views here.
def index(request):
    content = {}
    return render(request, 'analysis/analysis_base.html', content)


def refresh(request):
    content = {}
    return render(request, 'analysis/analysis_base.html', content)


def company(request):


    ticker = request.GET.get('ticker', '')  # 검색어
    context = {"ticker":ticker}
    
    if ticker.encode().isalpha():
        stock = yf.Ticker(ticker)
        price = pdr.get_data_yahoo(ticker)
        price['Date'] = price.index
        price['Date'] = price['Date'].dt.date  
        price.index = price['Date'].astype("str")
        price.drop(['Date'], axis=1, inplace=True)
        context['stock_price'] = price.T.to_json()
        context['last_stock_price'] = round(price.iloc[-1:,3:4].values[0][0], 2) 

        context['last_diff_val'] = round(price.diff().iloc[-1:,3:4].values[0][0], 2) 
        context['last_pct_val'] = round(price.pct_change().iloc[-1:,3:4].values[0][0] * 100, 2)
        recommand_df = stock.recommendations.loc['2023-01-01':, :]
        recommand_df['Date'] = recommand_df.index
        recommand_df = recommand_df[['Date', 'Firm', 'To Grade','From Grade','Action']]
        context['recommand_col'] = list(recommand_df.columns)
        context['recommand'] = recommand_df.T.to_dict()

        return render(request, 'main/company_detail.html', context)
    else:
        return render(request, 'main/company.html', context)



def today_check():
    #날짜 셋팅
    today = datetime.date.today()

