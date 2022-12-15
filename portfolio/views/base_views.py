from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator  
from django.db.models import Q

import yfinance as yf
import pandas as pd

from ..models import Portfolio, Stock
from ..forms import PortfolioForm, StockForm

from pymongo import MongoClient

from datetime import datetime, timedelta

from pymongo import MongoClient
import json

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']
infos_collection = db['infos']

def index(request):
    print(request.method)
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            port = form.save(commit=False)
            port.target_price = infos_collection.find_one({'ticker':request.POST.get('ticker')})
            port.create_date = timezone.now()
            port.author = request.user
            port.save()
            return redirect('portfolio:index')

    symbol = request.GET.get("ticker", "")
    context = {}
    context['ticker'] = symbol
    portfolio = Portfolio.objects.order_by('-create_date')
    if symbol:
        data = yf.Ticker(symbol)
        data_info = data.cashflow
        context['result'] = data_info.to_html
    context["portfolio"] = portfolio


    return render(request, 'port/portfolio_list.html', context)


def detail(request, port_id):
    port = get_object_or_404(Portfolio, pk=port_id)
    if len(port.stock_port.all()) > 0:
        port_value = 0
        for stock in port.stock_port.all():
            ticker = stock.ticker
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            last_quote = data['Close'].iloc[-1]
            stock.current_price = round(last_quote, 2)
            stock.profit = round(stock.current_price - stock.buy_price, 2)
            stock.return_ratio = round(stock.profit / stock.buy_price, 2) * 100
            stock.evaluated = round(stock.quantity * stock.current_price, 2)
            stock.save()
        port_value += stock.evaluated
    context = {'portfolio':port, "total_value" : round(port_value, 2)}
    return render(request, 'port/portfolio_detail.html', context)