from django.shortcuts import render
from pyfinviz.news import News

import pandas as pd
import requests
from bs4 import BeautifulSoup

def news_view(request, news_id):
    print(news_id)
    if news_id == 'fin':
        news = News()
        content = {'news_list':news.news_df}
    elif news_id == 'sec':
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
        content = {'news_list':df, 'press':news_id}

    return render(request, 'main/news.html', content)