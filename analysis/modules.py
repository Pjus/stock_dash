from pandas_datareader import data as pdr
from datetime import datetime, timedelta
from django.shortcuts import render
import yfinance as yf
import pandas as pd
import calendar
import json

from .models import FinancialEvent, FinEventDate

# News
from pyfinviz.news import News
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
import re

yf.pdr_override()



yesterday = datetime.now() - timedelta(1)
day = datetime.strftime(yesterday, '%Y-%m-%d')

today_origin = datetime.now()
today = datetime.strftime(today_origin, '%Y-%m-%d')


def make_price_query(ticker):
    price = pdr.get_data_yahoo(ticker)
    print(price)
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

# def get_price(ticker, yesterday):
#     print(ticker, yesterday)
#     week_of_day = calendar.day_name[today_origin.weekday()]
#     if check_none(ticker):
#         print("None")
#         price_mongodb_query = make_price_query(ticker)
#         price_collection.insert_one({'ticker':ticker, 'price' : price_mongodb_query})
#     else:
#         except_days = ['Monday', 'Sunday', 'Saturday']
#         last_day = get_last_day(ticker)
#         if week_of_day not in except_days :
#             if str(last_day) != str(yesterday):
#                 price_mongodb_query = make_price_query(ticker)
#                 price_collection.update_one({'ticker':ticker}, {'$set':{'price':price_mongodb_query }})
#         else:
#             if str(last_day) != str(yesterday):
#                 price_mongodb_query = make_price_query(ticker)
#                 price_collection.update_one({'ticker':ticker}, {'$set':{'price':price_mongodb_query }})

def get_currency(refresh=False):
    currency_query = {today:{}}
    df = pd.read_html('https://www.kita.net/cmmrcInfo/ehgtGnrlzInfo/rltmEhgt.do', header = 0, encoding='utf-8')[0]
    for row in df.iloc[:, :-1].iterrows():
        if row[1][3] < 0:
            numbers = re.sub(r'[^0-9.]', '', row[1][2])
            day_before = f'-{numbers}'
        else:
            numbers = re.sub(r'[^0-9.]', '', row[1][2])
            day_before = numbers

        currency_query[today][row[1][0].split(" ")[0]] = {
            'in_korean' : row[1][0].split(" ")[1],
            'current' : row[1][1],
            'day_before' : float(day_before),
            'change' : row[1][3],
            'buy' : row[1][4],
            'sell' : row[1][5],
            'send' : row[1][6],
            'receive' : row[1][7],
        }

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


def get_sec_news():
    url = 'https://www.sec.gov/news/pressreleases'
    df = pd.read_html(url)[0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = each.find('a')['href']
                links.append('https://www.sec.gov' + link)
            except:
                pass

    df['URL'] = links
    df['Time'] = df['Date'].str.replace('Date: ', '')
    df['Headline'] = df['Headline'].str.replace('Headline: ', '')
    df['URL'] = df['URL'].str.replace('Link: ', '')

    df = df[['Time', 'Headline', 'URL']]
    news_query = {}

    for row in df.iterrows():
        inner_query = {}
        inner_query['headline'] = row[1]['Headline']
        inner_query['url'] = row[1]['URL']
        news_query[row[1]['Time']] = inner_query



def get_finviz_news():
    news = News()
    df = news.news_df
    news_query = {}
    for idx, row in enumerate(df.iterrows()):
        now = datetime.now()
        now = datetime.strftime(today_origin, '%Y-%m-%d %H:%M')
        inner_query = {}
        inner_query['headline'] = row[1]['Headline']
        inner_query['url'] = row[1]['URL']
        inner_query['Time'] = row[1]['Time']
        news_query[f'{str(now)} {str(idx)}'] = inner_query

    



def get_calender():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    url = "https://kr.tradingview.com/economic-calendar/"

    driver = webdriver.Chrome("~/Downloads/chromedriver.exe", options=options)
    driver.get(url)
    driver.implicitly_wait(3)

    items = driver.find_elements(by=By.CLASS_NAME, value='economicCalendarItem-Q1EBfqP8')
    driver.implicitly_wait(1)
    event_day = driver.find_elements(by=By.CLASS_NAME, value='innerWrapper-sM9C7FZj')
    driver.implicitly_wait(1)

    date = []
    data_dict = {}


    for day in event_day:
        data_dict[day.text] = {}
        date.append(day.text)
        fin_event_date = FinEventDate(fin_current_date=day.text)
        fin_event_date.save()

    day_start = -1
    defalut_time = 24

    for item_idx, item in enumerate(items):
        temp_dict = {}

        country = item.find_element(by=By.CLASS_NAME, value='country-Q1EBfqP8')
        inner_html = country.get_attribute("innerHTML")
        

        all_data = item.text.split("\n")
       
        if ':' in all_data[0]:
            event_time = all_data[0]
            event_subject = all_data[1]

        else:
            if ':' in items[item_idx-1].text.split("\n")[0]:
                event_time = items[item_idx-1].text.split("\n")[0]
            else:
                event_time = items[item_idx-2].text.split("\n")[0]
            event_subject = all_data[0]

        if int(event_time.split(":")[0]) < defalut_time:
            day_start += 1
        defalut_time = int(event_time.split(":")[0])

        if "예측" in all_data:
            if all_data[-1] == '%':
                temp_dict['forecast'] = all_data[-5]
            else:
                temp_dict['forecast'] = all_data[-1]
        else:
            temp_dict['forecast'] = ''

        if "이전" in all_data:
            if all_data[-1] == '%':
                temp_dict['previous'] = all_data[-2]
            else:
                temp_dict['previous'] = all_data[-1]
        else:
            temp_dict['previous'] = ''



        fin_event = FinancialEvent(
                event_mother = fin_event_date, 
                img_src = inner_html[inner_html.find("https"):inner_html.find('"><')],
                country = re.compile('[가-힣]+').findall(inner_html)[0],
                event_time = event_time,
                event_date = date[day_start],
                event_subject = event_subject,
                forecast=temp_dict['forecast'],
                previous=temp_dict['previous'],

            )
        fin_event.save()

    
    for event in data_dict:
        print(event)
