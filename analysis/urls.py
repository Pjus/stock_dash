from django.urls import path

from .views import base_views, heatmap_view, main_dash_view, indicators_view, news_view

app_name = 'analysis'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('refresh/', base_views.refresh, name='refresh'),
    path('company/', base_views.company, name='company'),
    path('heatmap/', heatmap_view.get_heatmap, name='heatmap'),
    path('portable/', main_dash_view.get_portable, name='table'),
    path('mailing/', main_dash_view.get_mailing, name='mailing'),
    path('box/', main_dash_view.get_box, name='box'),
    path('indicator/macd/<str:ticker>/<int:day>', indicators_view.get_macd, name='macd'),
    path('indicator/bband/<str:ticker>', indicators_view.get_BBAND, name='bband'),
    path('indicator/rsi/<str:ticker>', indicators_view.get_RSI, name='rsi'),
    path('indicator/mfi/<str:ticker>', indicators_view.get_MFI, name='mfi'),
    path('indicator/atr/<str:ticker>', indicators_view.get_ATR, name='atr'),
    path('indicator/fi/<str:ticker>', indicators_view.get_Force_Index, name='fi'),
    path('indicator/evm/<str:ticker>', indicators_view.get_EMV, name='emv'),
    path('news/<str:news_id>/', news_view.index, name='news'),




]