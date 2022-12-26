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

yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')

week_of_day = calendar.day_name[today_origin.weekday()]

def board(request):
    nasdaq = "^IXIC"
    dow = "^DJI"
    last_day = list(price_collection.find_one({'ticker':nasdaq})['price'])[-1]
    if price_collection.find_one({'ticker':nasdaq}) != None:
        if week_of_day != "Monday":
            if str(last_day) != str(day):
                nas_price = pdr.get_data_yahoo("^IXIC")
                dow_price = pdr.get_data_yahoo("^DJI")

                nas_price_mongodb_query = {}
                for row in nas_price.iterrows():
                    nas_price_mongodb_query[str(row[0]).split(" ")[0]] = {
                        'High':row[1][0],
                        'Low':row[1][1],
                        'Open':row[1][2],
                        'Close':row[1][3],
                        'Adj Close':row[1][4],
                        'Volume':row[1][5],
                    }
                price_collection.update_one({'ticker':nasdaq}, {'$set':{'price':nas_price_mongodb_query }})
                
                
                dow_price_mongodb_query = {}
                for row in dow_price.iterrows():
                    dow_price_mongodb_query[str(row[0]).split(" ")[0]] = {
                        'High':row[1][0],
                        'Low':row[1][1],
                        'Open':row[1][2],
                        'Close':row[1][3],
                        'Adj Close':row[1][4],
                        'Volume':row[1][5],
                    }
                price_collection.update_one({'ticker':dow}, {'$set':{'price':dow_price_mongodb_query }})
    else:
        nas_price = pdr.get_data_yahoo(nasdaq)
        dow_price = pdr.get_data_yahoo(dow)
        nas_price_mongodb_query = {}
        for row in nas_price.iterrows():
            nas_price_mongodb_query[str(row[0]).split(" ")[0]] = {
                'High':row[1][0],
                'Low':row[1][1],
                'Open':row[1][2],
                'Close':row[1][3],
                'Adj Close':row[1][4],
                'Volume':row[1][5],
            }

        dow_price_mongodb_query = {}
        for row in dow_price.iterrows():
            dow_price_mongodb_query[str(row[0]).split(" ")[0]] = {
                'High':row[1][0],
                'Low':row[1][1],
                'Open':row[1][2],
                'Close':row[1][3],
                'Adj Close':row[1][4],
                'Volume':row[1][5],
            }
        price_collection.insert_one({'ticker':nasdaq, 'price' : nas_price_mongodb_query})
        price_collection.insert_one({'ticker':dow, 'price' : dow_price_mongodb_query})



    nas_price = price_collection.find_one({'ticker':nasdaq})['price']
    dow_price = price_collection.find_one({'ticker':dow})['price']
    currency = currency_collection.find_one({'date':today})['currency']

    nas_df = pd.DataFrame(nas_price).T.pct_change()
    dow_df = pd.DataFrame(dow_price).T.pct_change()

    krw = currency
    print(krw[today]['USD']['current'])
    

    context = {
        "nasdaq": round(nas_price[last_day]['Adj Close'], 2),
        "dow":round(dow_price[last_day]['Adj Close'], 2),
        "nas_pct": round(nas_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "dow_pct": round(dow_df.iloc[-1:, 3:4].values[0][0] * 100, 2),
        "currency": round(krw[today]['USD']['current'], 2),
        "currency_pct": krw[today]['USD']['change'],

    }
    if not request.user.is_authenticated:
        return render(request, 'main/articles.html', context)

    return render(request, 'main/core.html', context)


def get_portable(request):
    return render(request, 'main/tables.html')

def get_billing(request):
    return render(request, 'main/billing.html')

def get_box(request):
    return render(request, 'main/box.html')