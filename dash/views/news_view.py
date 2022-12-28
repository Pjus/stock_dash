from django.shortcuts import render
from pyfinviz.news import News

from analysis.modules import get_sec_news, time_in_range, get_collection, get_finviz_news
from datetime import time, datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time(7, 0, 0)
end = time(9, 0, 0)
now = datetime.now()

news_collection = get_collection("news")

def news_view(request, news_id):
    if news_id == 'fin':
        get_finviz_news()
        try:
            fin_news = news_collection.find_one({'press':news_id})['news']
        except:
            get_finviz_news()
            fin_news = news_collection.find_one({'press':news_id})['news']

        df = pd.DataFrame(fin_news).T
        
        content = {'news_list':df, 'press':news_id}

    elif news_id == 'sec':
        if time_in_range(start, end, now.time()):
            get_sec_news()
        try:
            sec_news = news_collection.find_one({'press':news_id})['news']
        except:
            get_sec_news()
            sec_news = news_collection.find_one({'press':news_id})['news']

        df = pd.DataFrame(sec_news).T
        df['Time'] = df.index

        content = {'news_list':df, 'press':news_id}

    return render(request, 'main/news.html', content)