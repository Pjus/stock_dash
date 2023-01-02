from django.shortcuts import render
import yfinance as yf
import json
from pymongo import MongoClient
from datetime import datetime, timedelta

import calendar

from analysis.modules import get_currency, get_price, get_finanacial_infos

yf.pdr_override()
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

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')

week_of_day = calendar.day_name[today_origin.weekday()]

# Create your views here.
def index(request):
    if currency_collection.find_one({'date':today}) == None:
        get_currency()
    currency = currency_collection.find_one({'date':today})['currency']
    content = {'currency' : currency, 'today':today }
    return render(request, 'analysis/analysis_base.html', content)


def refresh(request):
    get_currency(refresh=True)
    currency = currency_collection.find_one({'date':today})['currency']
    content = {'currency' : currency, 'today':today }
    return render(request, 'analysis/analysis_base.html', content)


def company(request):
    ticker = request.GET.get('ticker', '')  # 검색어
    content = {"ticker":ticker}

    if currency_collection.find_one({'date':today}) == None:
        get_currency()
    if ticker.encode().isalpha() == False:
        return render(request, 'main/company.html', content)

    if ticker.encode().isalpha():
        if infos_collection.find_one({'ticker':ticker}) == None:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            infos_collection.insert_one({'ticker':ticker, 'infos' : stock_info})

        get_price(ticker, yesterday)
        get_finanacial_infos(financial_collection, ticker, type="fs")
        get_finanacial_infos(balancesheet_collection, ticker, type="bs")
        get_finanacial_infos(cashflow_collection, ticker, type="cf")

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

        return render(request, 'main/company_detail.html', content)
    else:
        return render(request, 'main/company.html', content)





def today_check():
    #날짜 셋팅
    today = datetime.date.today()

