from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator  
from django.db.models import Q

from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd

from ..models import Portfolio, Stock
from ..forms import PortfolioForm, StockForm

from pymongo import MongoClient


import calendar

from datetime import datetime, timedelta, date
import calendar
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
price_collection = db['stock_price']

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

    today_month = date.today()
    last_month = today_month - timedelta(days=1)
    today_year = today_month.year

    today_month = today_month.strftime("%Y-%m").split("-")[1]
    last_month = last_month.strftime("%Y-%m").split("-")[1]

    port = get_object_or_404(Portfolio, pk=port_id)
    total_value = 0
    if len(port.stock_port.all()) > 0:
        port_value = {}
        for stock in port.stock_port.all():
            buy_year = stock.buy_dates.split("-")[0]
            ticker = stock.ticker
            stock_price = pdr.get_data_yahoo(ticker)
            new_df = stock_price.loc[stock.buy_dates:,]
            end_of_month = []
            for year in range(int(buy_year), int(today_year)+1):
                for i in range(1, 13):
                    input_dt = datetime(year, i, 13)
                    res = calendar.monthrange(input_dt.year, input_dt.month)
                    day = res[1]
                    end_of_month.append(f"{input_dt.year}-{input_dt.month}-{input_dt.day}")
            print(end_of_month)

            end_of_month_price = {}
            for day in end_of_month:
                try:
                    end_of_month_price[day] = new_df.loc[day,"Adj Close"][-1]
                except:
                    pass
            
            price_df = pd.DataFrame(end_of_month_price, index=['Close']).T

            price_df['buy_price'] = stock.buy_price
            price_df['profit'] = (price_df['Close'] - price_df['buy_price']) * stock.quantity
            profit_dict = price_df[['profit']].T.to_dict()

            json_val = json.dumps(profit_dict)
            stock.profit_history = json_val
            print(end_of_month)
            print(json_val)


            last_quote = new_df['Adj Close'].iloc[-1]
            stock.current_price = round(last_quote, 2)
            stock.profit = round((stock.current_price - stock.buy_price) * stock.quantity, 2)
            stock.evaluated = round(stock.quantity * stock.current_price, 2)
            stock.return_ratio = round((1 - (stock.buy_price / stock.current_price)) * 100, 2)
            stock.save()

            price_df = new_df[['Adj Close']]
            price_df['Current Value'] = price_df['Adj Close'] * stock.quantity
            price_df['Date'] = price_df.index
            price_df.index = price_df['Date'].apply(lambda x: x.date().strftime('%Y-%m-%d'))

            port_value[stock.ticker] = stock.evaluated
            total_value += stock.evaluated

        if port.port_history == "":
            history = {
                stock.ticker : price_df[['Current Value']].T.to_dict()
            }
            
            json_val = json.dumps(history)
            port.port_history = json_val
        else:
            port_dict = json.loads(port.port_history)
            port_dict[stock.ticker] = price_df[['Current Value']].T.to_dict()

            json_val = json.dumps(port_dict)
            port.port_history = json_val

        port.port_value = total_value
        total_value = round(total_value, 2)
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