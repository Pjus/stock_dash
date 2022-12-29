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

import json

today = datetime.now()
today = datetime.strftime(today, '%Y-%m-%d')
monthly_return = {

}

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']
infos_collection = db['infos']

def index(request):
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
    context = {"page":"Portfolio"}
    context['ticker'] = symbol
    portfolio = Portfolio.objects.order_by('-create_date')
    if symbol:
        data = yf.Ticker(symbol)
        data_info = data.cashflow
        context['result'] = data_info.to_html
    context["portfolio"] = portfolio
    print()


    return render(request, 'main/port_list.html', context)


def detail(request, port_id):
    port = get_object_or_404(Portfolio, pk=port_id)
    total_value = 0
    if len(port.stock_port.all()) > 0:
        port_value = 0
        port_profit = 0
        for stock in port.stock_port.all():
            print(stock.buy_dates)
            ticker = stock.ticker
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            last_quote = data['Close'].iloc[-1]
            stock.current_price = round(last_quote, 2)
            stock.profit = round(stock.current_price - stock.buy_price, 2)
            stock.return_ratio = round((stock.profit / stock.buy_price) * 100, 2)
            stock.evaluated = round(stock.quantity * stock.current_price, 2)
            stock.save()

            port_profit += stock.profit

        port_value += stock.evaluated
        if port.port_history == "":
            history = {
                today : port_value
            }
            json_val = json.dumps(history)
            port.port_history = json_val
        else:
            port_dict = json.loads(port.port_history)
            port_dict[today] = port_value
            json_val = json.dumps(port_dict)
            port.port_history = json_val

        port.port_value = port_value
        total_value = round(port_value, 2)
    else:
        port.port_value = 0
    port.save()
    context = {'portfolio':port, "total_value" : total_value, "page":"Portfolio"}
    return render(request, 'main/port_detail.html', context)


def port_delete(request, port_id):
    print(port_id)
    port = Portfolio.objects.get(id=port_id)
    port.delete()
    return redirect('portfolio:index')