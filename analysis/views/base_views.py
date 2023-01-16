from django.shortcuts import render
import yfinance as yf
import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd

import calendar

from analysis.modules import get_currency, get_price, get_finanacial_infos

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
    content = {"ticker":ticker}
    
    if ticker.encode().isalpha() == False:
        return render(request, 'main/company.html', content)

    if ticker.encode().isalpha():
        return render(request, 'main/company_detail.html', content)
    else:
        return render(request, 'main/company.html', content)



def today_check():
    #날짜 셋팅
    today = datetime.date.today()

