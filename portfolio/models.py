from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_portfolio')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title

class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stock_port')
    ticker = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    buy_price = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0, null=True)
    profit = models.FloatField(default=0, null=True)
    return_ratio = models.FloatField(default=0, null=True)
    volatility = models.FloatField(default=0, null=True)
    evaluated = models.FloatField(default=0, null=True)
    buy_dates = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.ticker

