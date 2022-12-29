from django.urls import path

from .views import base_views, port_view

app_name = 'portfolio'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('<int:port_id>/', base_views.detail, name='detail'),
    path('portfolio/delete/<int:port_id>/', base_views.port_delete, name="port_delete"),
    path('stock/create/<int:port_id>/', port_view.stock_create, name="stock_create"),
    path('stock/delete/<int:port_id>/<int:stock_id>/', port_view.stock_delete, name="stock_delete")

    
]