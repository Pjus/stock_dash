from pandas_datareader import data as pdr
from datetime import datetime, timedelta
from django.shortcuts import render
from pymongo import MongoClient
import yfinance as yf
import pandas as pd
import calendar
import json

yf.pdr_override()
with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']

price_collection = db['stock_price']
currency_collection = db['currency']

balancesheet_collection = db['balance']
cashflow_collection = db['cashflow']
financial_collection = db['financial_statement']
price_collection = db['stock_price']
infos_collection = db['infos']

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')

def get_last_day(ticker):
    last_day = list(price_collection.find_one({'ticker':ticker})['price'])[-1]
    return last_day

def check_none(ticker):
    return price_collection.find_one({'ticker':ticker}) == None

def make_price_query(ticker):
    price = pdr.get_data_yahoo(ticker)
    price_mongodb_query = {}
    for row in price.iterrows():
        price_mongodb_query[str(row[0]).split(" ")[0]] = {
            'High':row[1][0],
            'Low':row[1][1],
            'Open':row[1][2],
            'Close':row[1][3],
            'Adj Close':row[1][4],
            'Volume':row[1][5],
        }
    return price_mongodb_query

def get_price(ticker, yesterday):
    week_of_day = calendar.day_name[today_origin.weekday()]
    if check_none(ticker):
        print("None")
        price_mongodb_query = make_price_query(ticker)
        price_collection.insert_one({'ticker':ticker, 'price' : price_mongodb_query})
    else:
        except_days = ['Monday', 'Sunday', 'Saturday']
        if week_of_day not in except_days :
            print(week_of_day)
            last_day = get_last_day(ticker)
            if str(last_day) != str(yesterday):
                print(last_day)
                price_mongodb_query = make_price_query(ticker)
                price_collection.update_one({'ticker':ticker}, {'$set':{'price':price_mongodb_query }})
        else:
            pass

def get_currency(refresh=False):
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
    if refresh:
        currency_collection.insert_one({'date':today, 'currency' : currency_query})
    elif refresh:
        currency_collection.update_one({'date':today}, {'$set':{'currency' : currency_query}})


def get_finanacial_infos(collection, ticker, type):
    stock = yf.Ticker(ticker)
    if collection.find_one({'ticker':ticker}) == None:
        financial = stock.quarterly_cashflow
        financial.fillna(0, inplace=True)
        mongodb_query = {}
        for idx, row in enumerate(financial.items()):
            date = str(row[0]).split(" ")[0]
            mongodb_query[date] = {}
            for i in range(len(financial)):
                subject = financial.index[i]
                column = financial.columns[idx]
                mongodb_query[date][subject] = financial[column][subject]
        collection.insert_one({'ticker':ticker, type : mongodb_query})



def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end