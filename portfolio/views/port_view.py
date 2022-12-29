from django.shortcuts import render, get_object_or_404, redirect
import json

from ..forms import StockForm
from ..models import Stock, Portfolio

def stock_create(request, port_id):
    port = get_object_or_404(Portfolio, pk=port_id)
    form = StockForm(request.POST)
    if form.is_valid():
        ticker = request.POST.get('ticker')
        buy_price = float(request.POST.get('buy_price'))
        quantity = int(request.POST.get('quantity'))
        buy_date = request.POST.get('datepicker')

        stock_list = Stock.objects.filter(portfolio=port_id, ticker=ticker)
        if len(stock_list) != 0:
            stocks = stock_list
            total_price = stocks.buy_price * stocks.quantity
            new_price = buy_price * quantity
            total_quantity = stocks.quantity + quantity
            stocks.buy_price = (total_price + new_price) / total_quantity
            stocks.quantity += quantity
            stocks.save()
        else:
            stocks = Stock(portfolio=port, ticker=ticker, quantity=quantity, buy_price=buy_price, buy_dates=buy_date)
            stocks.save()
        return redirect('portfolio:detail', port_id)
    else:
        print("fail")
        return redirect('portfolio:detail', port_id)


def stock_delete(request, port_id, stock_id):
    stock = Stock.objects.get(id=stock_id)
    stock.delete()
    return redirect('portfolio:detail', port_id)
