from django.shortcuts import render
from pyfinviz.news import News


def news_view(request):
    news = News()
    content = {'news_list':news.news_df}
    return render(request, 'dash/news.html', content)