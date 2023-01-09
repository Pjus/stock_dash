from django.urls import path

from .views import base_views, heatmap_view, main_dash_view, indicators_view

app_name = 'analysis'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('refresh/', base_views.refresh, name='refresh'),
    path('company/', base_views.company, name='company'),
    path('heatmap/', heatmap_view.get_heatmap, name='heatmap'),
    path('portable/', main_dash_view.get_portable, name='table'),
    path('billing/', main_dash_view.get_billing, name='billing'),
    path('box/', main_dash_view.get_box, name='box'),
    path('indicator/macd/<str:ticker>/<int:day>', indicators_view.get_macd, name='macd'),
    path('indicator/bband/<str:ticker>', indicators_view.get_BBAND, name='bband'),


]