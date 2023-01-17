from datetime import datetime, timedelta, time
from django.shortcuts import render
from django.db.models import Q

from analysis.modules import get_calender
from portfolio.models import Portfolio

import yfinance as yf
import pandas as pd
import json
import re
from pandas_datareader import data as pdr

from ..models import FinEventDate, FinancialEvent, FinNews

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

    event_list = FinEventDate.objects.order_by('-fin_current_date')
    news_list = FinNews.objects.order_by('date')
    sec_news_list = news_list.filter(Q(press="sec")).distinct()
    context['news_list'] = sec_news_list

    if len(event_list) == 0:
        get_calender()
        event_list = FinEventDate.objects.order_by('-fin_current_date')
        event_detail = FinancialEvent.objects.order_by('event_mother')
        print(len(event_list))
        context['event_list'] = event_list
        context['event_detail_list'] = event_detail
    else:
        event_list = FinEventDate.objects.order_by('fin_current_date')
        event_detail = FinancialEvent.objects.order_by('event_mother')

        context['event_list'] = event_list
        context['event_detail_list'] = event_detail

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