from django.db import models
from django.contrib.auth.models import User



class FinEventDate(models.Model):
    fin_current_date = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.fin_current_date


class FinancialEvent(models.Model):
    event_mother = models.ForeignKey("FinEventDate", on_delete=models.CASCADE, related_name='event_date')
    img_src = models.CharField(max_length=500, default='')
    country = models.CharField(max_length=10, default='')
    event_time = models.CharField(max_length=10, default='')
    event_date = models.CharField(max_length=10, default='')
    event_subject = models.CharField(max_length=100, default='')
    forecast = models.CharField(max_length=10, default='')
    previous = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.country


class FinNews(models.Model):
    press = models.CharField(max_length=10, default='')
    title = models.CharField(max_length=50, default='')
    url = models.CharField(max_length=100, default='')
    date = models.CharField(max_length=20, default='')
   
    def __str__(self):
        return self.title


class StockCompany(models.Model):
    ticker = models.CharField(max_length=5, default='')
    company_name = models.CharField(max_length=20, default='')
    industry = models.CharField(max_length=20, default='')
    market_cap = models.IntegerField(blank=True, default=0)
    recommandtion = models.CharField(max_length=5, default='', blank=True)
    def __str__(self):
        return self.ticker

class CompanyPrice(models.Model):
    ticker = models.ForeignKey("StockCompany", on_delete=models.CASCADE, related_name='company_ticker')
    date = models.CharField(max_length=10)
    open_price = models.FloatField(default=0, blank=True)
    high_price = models.FloatField(default=0, blank=True)
    low_price = models.FloatField(default=0, blank=True)
    close_price = models.FloatField(default=0, blank=True)
    adj_close_price = models.FloatField(default=0, blank=True)
    volume = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.ticker.ticker


class Currency(models.Model):
    date = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    in_korean = models.CharField(max_length=10)
    current = models.FloatField(default=0, blank=True)
    day_before = models.FloatField(default=0, blank=True)
    change = models.FloatField(default=0, blank=True)
    buy = models.FloatField(default=0, blank=True)
    sell = models.FloatField(default=0, blank=True)
    send = models.FloatField(default=0, blank=True)
    receive = models.FloatField(default=0, blank=True)
    
    def __str__(self):
        return self.country


class MailingTicker(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing_user')
    ticker = models.CharField(max_length=10, default='')
    create_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ticker

