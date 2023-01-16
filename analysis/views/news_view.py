from django.shortcuts import render
from pyfinviz.news import News

from datetime import time, datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time(7, 0, 0)
end = time(9, 0, 0)
now = datetime.now()


def index(request, news_id):
    content = {}
    return render(request, 'main/news.html', content)