from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

import yfinance as yf
from pandas_datareader import data as pdr
import json

# Create your views here.
def index(request):
    return render(request, 'analysis/analysis_base.html')


def company(request):
    ticker = request.GET.get('ticker', '')  # 검색어
    stock = yf.Ticker(ticker)
    content = {"ticker":ticker}
    if ticker != '':
        stock_price = pdr.get_data_yahoo(ticker)[-300:]
        stock_price.reset_index(inplace=True)
        stock_price['Date'] = stock_price['Date'].astype("string")
        stock_price = stock_price.to_json()

        qt_fs = stock.quarterly_financials.T
        qt_fs['Date'] = qt_fs.index
        qt_fs['Date'] = qt_fs['Date'].astype('string')
        qt_fs.reset_index(inplace=True)
        qt_fs = qt_fs.to_json()

        
        content = {"ticker":ticker, 'stock_price':stock_price, 'financial':qt_fs}


    return render(request, 'analysis/comany.html', content)