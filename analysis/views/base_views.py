from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

import yfinance as yf
from pandas_datareader import data as pdr
import json
from pymongo import MongoClient

from datetime import datetime, timedelta

client = MongoClient('mongodb://jun:qkrwns716722!@0.0.0.0', 27017)
db = client['stockDB']

balancesheet_collection = db['balance']
cashflow_collection = db['cashflow']
financial_collection = db['financial_statement']
price_collection = db['stock_price']
infos_collection = db['infos']

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

# Create your views here.
def index(request):
    return render(request, 'analysis/analysis_base.html')


def company(request):
    ticker = request.GET.get('ticker', '')  # 검색어
    stock = yf.Ticker(ticker)
    content = {"ticker":ticker}
    if ticker.encode().isalpha() == False:
        print("not alpha")
        return render(request, 'analysis/company.html', content)

    if ticker.encode().isalpha():
        print("alpha")
        # last_day = list(price_collection.find_one({'ticker':ticker})['price'])[-1]
        # if last_day != day:
        #     stock_price = pdr.get_data_yahoo(ticker)
        #     stock_price = stock_price.iloc[-1,:]
        #     price_mongodb_query = {}
        #     price_collection.update_one({'ticker':ticker, 'price' : price_mongodb_query})
        if infos_collection.find_one({'ticker':ticker}) == None:
            stock_info = stock.info
            infos_collection.insert_one({'ticker':ticker, 'infos' : stock_info})

        if price_collection.find_one({'ticker':ticker}) == None:
            stock_price = pdr.get_data_yahoo(ticker)
            price_mongodb_query = {}
            for row in stock_price.iterrows():
                price_mongodb_query[str(row[0]).split(" ")[0]] = {
                    'High':row[1][0],
                    'Low':row[1][1],
                    'Open':row[1][2],
                    'Close':row[1][3],
                    'Volume':row[1][4],
                    'Adj Close':row[1][5],
                }
            price_collection.insert_one({'ticker':ticker, 'price' : price_mongodb_query})

        if financial_collection.find_one({'ticker':ticker}) == None:
            qt_fs = stock.quarterly_financials
            qt_fs.fillna(0, inplace=True)
            fs_mongodb_query = {}
            for row in qt_fs.items():
                date = str(row[0]).split(" ")[0]
                fs_mongodb_query[date] = {}
                for i in range(len(qt_fs)):
                    subject = qt_fs.index[i]
                    fs_mongodb_query[date][subject] = qt_fs[date][subject]
            financial_collection.insert_one({'ticker':ticker, 'fs' : fs_mongodb_query})


        if balancesheet_collection.find_one({'ticker':ticker}) == None:
            qt_bs = stock.quarterly_balancesheet
            qt_bs.fillna(0, inplace=True)
            bs_mongodb_query = {}
            for row in qt_bs.items():
                date = str(row[0]).split(" ")[0]
                bs_mongodb_query[date] = {}
                for i in range(len(qt_bs)):
                    subject = qt_bs.index[i]
                    bs_mongodb_query[date][subject] = qt_bs[date][subject]
            balancesheet_collection.insert_one({'ticker':ticker, 'bs' : bs_mongodb_query})


        if cashflow_collection.find_one({'ticker':ticker}) == None:
            qt_cf = stock.quarterly_cashflow
            qt_cf.fillna(0, inplace=True)
            cf_mongodb_query = {}
            for row in qt_cf.items():
                date = str(row[0]).split(" ")[0]
                cf_mongodb_query[date] = {}
                for i in range(len(qt_cf)):
                    subject = qt_cf.index[i]
                    cf_mongodb_query[date][subject] = qt_cf[date][subject]
            cashflow_collection.insert_one({'ticker':ticker, 'cf' : cf_mongodb_query})

        stock_price = price_collection.find_one({'ticker':ticker})['price']
        fs = financial_collection.find_one({'ticker':ticker})['fs']
        bs = balancesheet_collection.find_one({'ticker':ticker})['bs']
        cf = cashflow_collection.find_one({'ticker':ticker})['cf']
        infos = infos_collection.find_one({'ticker':ticker})['infos']
        
        content = {
            "ticker":ticker, 
            'stock_price':json.dumps(stock_price), 
            'financial':json.dumps(fs), 
            'balance':json.dumps(bs), 
            'cashflow':json.dumps(cf), 
            'dict_fs':fs,
            'dict_bs':bs,
            'dict_cf':cf,
            'len_fs':len(list(fs.values())[0]) // 2,
            'len_bs':len(list(bs.values())[0]) // 2,
            'len_cf':len(list(cf.values())[0]) // 2,
            'infos':infos,
        }


    return render(request, 'analysis/company.html', content)