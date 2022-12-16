from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

import yfinance as yf
from pandas_datareader import data as pdr
import json
from pymongo import MongoClient

from datetime import datetime, timedelta

from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)


client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']

balancesheet_collection = db['balance']
cashflow_collection = db['cashflow']
financial_collection = db['financial_statement']
price_collection = db['stock_price']
infos_collection = db['infos']
currency_collection = db['currency']

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')


today = datetime.now()
today = datetime.strftime(today, '%Y-%m-%d')
# Create your views here.
def index(request):
    if currency_collection.find_one({'date':today}) == None:
        currency_query = {today:{}}
        df = pd.read_html('https://www.kita.net/cmmrcInfo/ehgtGnrlzInfo/rltmEhgt.do', header = 0, encoding='utf-8')[0]
        for row in df.iloc[:, :-1].iterrows():
            currency_query[today][row[1][0].split(" ")[0]] = {
                'in_korean' : row[1][0].split(" ")[1],
                'current' : row[1][1],
                'day_before' : row[1][2],
                'change' : row[1][3],
                'buy' : row[1][4],
                'sell' : row[1][5],
                'send' : row[1][6],
                'receive' : row[1][7],
            }
        currency_collection.insert_one({'date':today, 'currency' : currency_query})
    currency = currency_collection.find_one({'date':today})['currency']
    content = {'currency' : currency, 'today':today }
    return render(request, 'analysis/analysis_base.html', content)


def refresh(request):
    currency_query = {today:{}}
    df = pd.read_html('https://www.kita.net/cmmrcInfo/ehgtGnrlzInfo/rltmEhgt.do', header = 0, encoding='utf-8')[0]
    for row in df.iloc[:, :-1].iterrows():
        currency_query[today][row[1][0].split(" ")[0]] = {
            'in_korean' : row[1][0].split(" ")[1],
            'current' : row[1][1],
            'day_before' : row[1][2],
            'change' : row[1][3],
            'buy' : row[1][4],
            'sell' : row[1][5],
            'send' : row[1][6],
            'receive' : row[1][7],
        }
    currency_collection.update_one({'date':today}, {'$set':{'currency' : currency_query}})
    currency = currency_collection.find_one({'date':today})['currency']
    content = {'currency' : currency, 'today':today }
    return render(request, 'analysis/analysis_base.html', content)


def company(request):
    ticker = request.GET.get('ticker', '')  # 검색어
    stock = yf.Ticker(ticker)
    content = {"ticker":ticker}

    if currency_collection.find_one({'date':today}) == None:
        currency_query = {today:{}}
        df = pd.read_html('https://www.kita.net/cmmrcInfo/ehgtGnrlzInfo/rltmEhgt.do', header = 0, encoding='utf-8')[0]
        for row in df.iloc[:, :-1].iterrows():
            currency_query[today][row[1][0].split(" ")[0]] = {
                'in_korean' : row[1][0].split(" ")[1],
                'current' : row[1][1],
                'day_before' : row[1][2],
                'change' : row[1][3],
                'buy' : row[1][4],
                'sell' : row[1][5],
                'send' : row[1][6],
                'receive' : row[1][7],
            }
        
        currency_collection.insert_one({'date':today, 'currency' : currency_query})

    if ticker.encode().isalpha() == False:
        return render(request, 'analysis/company.html', content)

    if ticker.encode().isalpha():
        if infos_collection.find_one({'ticker':ticker}) == None:
            stock_info = stock.info
            infos_collection.insert_one({'ticker':ticker, 'infos' : stock_info})

        if price_collection.find_one({'ticker':ticker}) != None:
            last_day = list(price_collection.find_one({'ticker':ticker})['price'])[-1]
            if str(last_day) != str(day):
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
                price_collection.update_one({'ticker':ticker}, {'$set':{'price':price_mongodb_query }})

        else:
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
            for idx, row in enumerate(qt_fs.items()):
                date = str(row[0]).split(" ")[0]
                fs_mongodb_query[date] = {}
                for i in range(len(qt_fs)):
                    subject = qt_fs.index[i]
                    column = qt_fs.columns[idx]
                    fs_mongodb_query[date][subject] = qt_fs[column][subject]
            financial_collection.insert_one({'ticker':ticker, 'fs' : fs_mongodb_query})


        if balancesheet_collection.find_one({'ticker':ticker}) == None:
            qt_bs = stock.quarterly_balancesheet
            qt_bs.fillna(0, inplace=True)
            bs_mongodb_query = {}
            for idx, row in enumerate(qt_bs.items()):
                date = str(row[0]).split(" ")[0]
                bs_mongodb_query[date] = {}
                for i in range(len(qt_bs)):
                    subject = qt_bs.index[i]
                    column = qt_bs.columns[idx]
                    bs_mongodb_query[date][subject] = qt_bs[column][subject]
            balancesheet_collection.insert_one({'ticker':ticker, 'bs' : bs_mongodb_query})


        if cashflow_collection.find_one({'ticker':ticker}) == None:
            qt_cf = stock.quarterly_cashflow
            qt_cf.fillna(0, inplace=True)
            cf_mongodb_query = {}
            for idx, row in enumerate(qt_cf.items()):
                date = str(row[0]).split(" ")[0]
                cf_mongodb_query[date] = {}
                for i in range(len(qt_cf)):
                    subject = qt_cf.index[i]
                    column = qt_cf.columns[idx]
                    cf_mongodb_query[date][subject] = qt_cf[column][subject]
            cashflow_collection.insert_one({'ticker':ticker, 'cf' : cf_mongodb_query})

        stock_price = price_collection.find_one({'ticker':ticker})['price']
        fs = financial_collection.find_one({'ticker':ticker})['fs']
        bs = balancesheet_collection.find_one({'ticker':ticker})['bs']
        cf = cashflow_collection.find_one({'ticker':ticker})['cf']
        infos = infos_collection.find_one({'ticker':ticker})['infos']
        currency = currency_collection.find_one({'date':today})['currency']

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
            'currency':currency[today]['USD']['current'],
            'current_krw':format(round(infos['currentPrice'] * currency[today]['USD']['current']), ',')
        }


    return render(request, 'analysis/company.html', content)