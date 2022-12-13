import yfinance as yf
from pandas_datareader import data as pdr
import json
from pymongo import MongoClient

from datetime import datetime, timedelta
from yahoo_fin import stock_info as si

client = MongoClient('mongodb://jun:qkrwns716722!@0.0.0.0', 27017)
db = client['stockDB']

balancesheet_collection = db['balance']
cashflow_collection = db['cashflow']
financial_collection = db['financial_statement']
price_collection = db['stock_price']
infos_collection = db['infos']


def company(ticker):
    stock = yf.Ticker(ticker)
    if ticker.isalpha():
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
            cf_mongodb_query = {}
            for row in qt_cf.items():
                date = str(row[0]).split(" ")[0]
                cf_mongodb_query[date] = {}
                for i in range(len(qt_cf)):
                    subject = qt_cf.index[i]
                    cf_mongodb_query[date][subject] = qt_cf[date][subject]
            cashflow_collection.insert_one({'ticker':ticker, 'cf' : cf_mongodb_query})

# tickers = si.tickers_sp500()

# for ticker in tickers:
#     print(ticker)
#     company(ticker)


# db.balance.drop()
# db.cashflow.drop()
# db.financial_statement.drop()
# db.stock_price.drop()
# db.infos.drop()

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')
if price_collection.find_one({'ticker':"msft"}) != None:
    last_day = list(price_collection.find_one({'ticker':"msft"})['price'])[-1]
    if str(last_day) != str(day):
        print("???")
        stock_price = pdr.get_data_yahoo("msft")
        stock_price = stock_price.iloc[-1,:]
        price_mongodb_query = {}
        price_mongodb_query[str(stock_price.name).split(" ")[0]] = {
            'High':stock_price['High'],
            'Low':stock_price['Low'],
            'Open':stock_price['Open'],
            'Close':stock_price['Close'],
            'Volume':stock_price['Volume'],
            'Adj Close':stock_price['Adj Close'],
        }
        print(price_mongodb_query)
        price_collection.update({'ticker':ticker}, {'$push':{'price' : price_mongodb_query}})