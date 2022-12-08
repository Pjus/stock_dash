from django import forms
from .models import Portfolio, Stock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio  # 사용할 모델
        fields = ['title']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock  # 사용할 모델
        fields = ['ticker', 'buy_price', 'quantity'] 

