from django.shortcuts import render, get_object_or_404, redirect

from ..forms import StockForm
from ..models import Stock, Portfolio

def stock_create(request, port_id):
    port = get_object_or_404(Portfolio, pk=port_id)
    form = StockForm(request.POST)
    if form.is_valid():
        stock_list = Stock.objects.filter(portfolio=port, ticker=request.POST.get('ticker'))
        if len(stock_list) > 0:
            stocks = stock_list[0]
            stocks.buy_price = (stocks.buy_price * stocks.quantity + float(request.POST.get('buy_price'))) * int(request.POST.get('quantity')) / (stocks.quantity + int(request.POST.get('quantity')))
            stocks.quantity += int(request.POST.get('quantity'))
            stocks.save()
        else:
            stocks = Stock(portfolio=port, ticker=request.POST.get('ticker'), quantity=request.POST.get('quantity'), buy_price=request.POST.get('buy_price'))
            stocks.save()
        return redirect('portfolio:detail', port_id)
    else:
        print("fail")
        return redirect('portfolio:detail', port_id)


def stock_delete(request, port_id, stock_id):
    stock = Stock.objects.get(id=stock_id)
    stock.delete()
    return redirect('portfolio:detail', port_id)
