from django.shortcuts import render
from django.db.models import Q

from datetime import time, datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from ..models import FinNews
from ..modules import get_finviz_news, get_sec_news
start = time(7, 0, 0)
end = time(9, 0, 0)
now = datetime.now()


def index(request, news_id):
    content = {}
    if news_id == "fin":
        news_list = FinNews.objects.order_by('date')

        if len(news_list) < 1:
            get_finviz_news()

        fin_news_list = news_list = news_list.filter(Q(press="fin")).distinct()
        content['news_list'] = fin_news_list
        content['press'] = 'Finviz'

    elif news_id == 'sec':
        news_list = FinNews.objects.order_by('date')
        news_list = news_list.filter(Q(press="sec")).distinct()

        if len(news_list) < 1:
            get_sec_news()

        sec_news_list = news_list.filter(Q(press="sec")).distinct()
        content['news_list'] = sec_news_list
        content['press'] = 'SEC'

    return render(request, 'main/news.html', content)