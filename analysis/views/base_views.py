from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

import yfinance as yf
from pandas_datareader import data as pdr
import json
from pymongo import MongoClient

from datetime import datetime, timedelta

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = MongoClient(sc_python['MONGODB'])
db = client['stockDB']

balancesheet_collection = db['balance']
cashflow_collection = db['cashflow']
financial_collection = db['financial_statement']
price_collection = db['stock_price']

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')
# Create your views here.
def index(request):
    return render(request, 'analysis/analysis_base.html')


def company(request):
    ticker = request.GET.get('ticker', '')  # 검색어
    stock = yf.Ticker(ticker)
    content = {"ticker":ticker}
    if ticker != '':
        last_day = list(price_collection.find_one({'ticker':ticker})['price'])[-1]
        # if last_day != day:
        #     stock_price = pdr.get_data_yahoo(ticker)
        #     stock_price = stock_price.iloc[-1,:]
        #     price_mongodb_query = {}
        #     price_collection.update_one({'ticker':ticker, 'price' : price_mongodb_query})

        if price_collection.find_one({'ticker':ticker}) == None:
            stock_price = pdr.get_data_yahoo(ticker)[-300:]
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
            fs_mongodb_query = {}
            for row in qt_fs.items():
                fs_mongodb_query[str(row[0]).split(" ")[0]] = {
                    row[1].index[0] : str(row[1][0]),
                    row[1].index[1] : str(row[1][1]),
                    row[1].index[2] : str(row[1][2]),
                    row[1].index[3] : str(row[1][3]),
                    row[1].index[4] : str(row[1][4]),
                    row[1].index[5] : str(row[1][5]),
                    row[1].index[6] : str(row[1][6]),
                    row[1].index[7] : str(row[1][7]),
                    row[1].index[8] : str(row[1][8]),
                    row[1].index[9] : str(row[1][9]),
                    row[1].index[10] : str(row[1][10]),
                    row[1].index[11] : str(row[1][11]),
                    row[1].index[12] : str(row[1][12]),
                    row[1].index[13] : str(row[1][13]),
                    row[1].index[14] : str(row[1][14]),
                    row[1].index[15] : str(row[1][15]),
                    row[1].index[16] : str(row[1][16]),
                    row[1].index[17] : str(row[1][17]),
                    row[1].index[18] : str(row[1][18]),
                    row[1].index[19] : str(row[1][19]),
                    row[1].index[20] : str(row[1][20]),
                    row[1].index[21] : str(row[1][21]),
                }
            financial_collection.insert_one({'ticker':ticker, 'fs' : fs_mongodb_query})


        if balancesheet_collection.find_one({'ticker':ticker}) == None:
            qt_bs = stock.quarterly_balancesheet
            bs_mongodb_query = {}
            for row in qt_bs.items():
                bs_mongodb_query[str(row[0]).split(" ")[0]] = {
                    row[1].index[0] : str(row[1][0]),
                    row[1].index[1] : str(row[1][1]),
                    row[1].index[2] : str(row[1][2]),
                    row[1].index[3] : str(row[1][3]),
                    row[1].index[4] : str(row[1][4]),
                    row[1].index[5] : str(row[1][5]),
                    row[1].index[6] : str(row[1][6]),
                    row[1].index[7] : str(row[1][7]),
                    row[1].index[8] : str(row[1][8]),
                    row[1].index[9] : str(row[1][9]),
                    row[1].index[10] : str(row[1][10]),
                    row[1].index[11] : str(row[1][11]),
                    row[1].index[12] : str(row[1][12]),
                    row[1].index[13] : str(row[1][13]),
                    row[1].index[14] : str(row[1][14]),
                    row[1].index[15] : str(row[1][15]),
                    row[1].index[16] : str(row[1][16]),
                    row[1].index[17] : str(row[1][17]),
                    row[1].index[18] : str(row[1][18]),
                    row[1].index[19] : str(row[1][19]),
                    row[1].index[20] : str(row[1][20]),
                    row[1].index[21] : str(row[1][21]),
                    row[1].index[22] : str(row[1][22]),

                }
            balancesheet_collection.insert_one({'ticker':ticker, 'bs' : bs_mongodb_query})


        if cashflow_collection.find_one({'ticker':ticker}) == None:
            qt_cf = stock.quarterly_cashflow
            cf_mongodb_query = {}
            for row in qt_cf.items():
                cf_mongodb_query[str(row[0]).split(" ")[0]] = {
                    row[1].index[0] : str(row[1][0]),
                    row[1].index[1] : str(row[1][1]),
                    row[1].index[2] : str(row[1][2]),
                    row[1].index[3] : str(row[1][3]),
                    row[1].index[4] : str(row[1][4]),
                    row[1].index[5] : str(row[1][5]),
                    row[1].index[6] : str(row[1][6]),
                    row[1].index[7] : str(row[1][7]),
                    row[1].index[8] : str(row[1][8]),
                    row[1].index[9] : str(row[1][9]),
                    row[1].index[10] : str(row[1][10]),
                    row[1].index[11] : str(row[1][11]),
                    row[1].index[12] : str(row[1][12]),
                    row[1].index[13] : str(row[1][13]),
                    row[1].index[14] : str(row[1][14]),
                    row[1].index[15] : str(row[1][15]),
                    row[1].index[16] : str(row[1][16]),
                    row[1].index[17] : str(row[1][17]),
                }
            cashflow_collection.insert_one({'ticker':ticker, 'cf' : cf_mongodb_query})


        stock_price = price_collection.find_one({'ticker':ticker})['price']
        fs = financial_collection.find_one({'ticker':ticker})['fs']
        bs = balancesheet_collection.find_one({'ticker':ticker})['bs']
        cf = cashflow_collection.find_one({'ticker':ticker})['cf']


        content = {
            "ticker":ticker, 
            'stock_price':json.dumps(stock_price), 
            'financial':json.dumps(fs), 
            'balance':json.dumps(bs), 
            'cashflow':json.dumps(cf), 
            'dict_fs':fs,
            'dict_bs':bs,
            'dict_cf':cf,
        
        }


    return render(request, 'analysis/company.html', content)