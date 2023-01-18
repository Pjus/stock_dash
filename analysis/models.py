from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



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
    sector = models.CharField(max_length=20, default='')
    industry = models.CharField(max_length=50, default='')
    market_cap = models.IntegerField(default=0, blank=True)
    recommandation = models.CharField(max_length=5, default='', blank=True)
    last_price = models.FloatField(default=0, blank=True)

    targetLowPrice = models.FloatField(default=0, blank=True)
    target_mean_price = models.FloatField(default=0, blank=True)
    targetHighPrice = models.FloatField(default=0, blank=True)
    targetMedianPrice = models.FloatField(default=0, blank=True)
    
    ebitdaMargins = models.FloatField(default=0, blank=True)
    profitMargins = models.FloatField(default=0, blank=True)
    grossMargins = models.FloatField(default=0, blank=True)
    operatingMargins = models.FloatField(default=0, blank=True)

    operatingCashflow = models.FloatField(default=0, blank=True)
    revenueGrowth = models.FloatField(default=0, blank=True)
    ebitda = models.FloatField(default=0, blank=True)

    grossProfits = models.FloatField(default=0, blank=True)
    freeCashflow = models.FloatField(default=0, blank=True)

    earningsGrowth = models.FloatField(default=0, blank=True)
    currentRatio = models.FloatField(default=0, blank=True)
    returnOnAssets = models.FloatField(default=0, blank=True)

    debtToEquity = models.FloatField(default=0, blank=True)
    returnOnEquity = models.FloatField(default=0, blank=True)
    totalCash = models.FloatField(default=0, blank=True)
    totalDebt = models.FloatField(default=0, blank=True)

    totalRevenue = models.FloatField(default=0, blank=True)
    totalCashPerShare = models.FloatField(default=0, blank=True)
    revenuePerShare = models.FloatField(default=0, blank=True)


    quickRatio = models.FloatField(default=0, blank=True)
    enterpriseToRevenue = models.FloatField(default=0, blank=True)
    enterpriseToEbitda = models.FloatField(default=0, blank=True)
    WeekChange = models.FloatField(default=0, blank=True)


    forwardEps = models.FloatField(default=0, blank=True)
    sharesOutstanding = models.IntegerField(default=0, blank=True)
    bookValue = models.FloatField(default=0, blank=True)
    sharesShort = models.IntegerField(default=0, blank=True)

    sharesPercentSharesOut = models.FloatField(default=0, blank=True)
    heldPercentInstitutions = models.FloatField(default=0, blank=True)
    netIncomeToCommon = models.IntegerField(default=0, blank=True)
    trailingEps = models.FloatField(default=0, blank=True)

    lastDividendValue = models.FloatField(default=0, blank=True)
    priceToBook = models.FloatField(default=0, blank=True)
    heldPercentInsiders = models.FloatField(default=0, blank=True)
    shortRatio = models.FloatField(default=0, blank=True)
    floatShares = models.FloatField(default=0, blank=True)
    beta = models.FloatField(default=0, blank=True)
    enterpriseValue = models.FloatField(default=0, blank=True)
    earningsQuarterlyGrowth = models.FloatField(default=0, blank=True)
    priceToSalesTrailing12Months = models.FloatField(default=0, blank=True)


    pegRatio = models.FloatField(default=0, blank=True)
    forwardPE = models.FloatField(default=0, blank=True)
    shortPercentOfFloat = models.FloatField(default=0, blank=True)
    sharesShortPriorMonth = models.IntegerField(default=0, blank=True)
    twoHundredDayAverage = models.FloatField(default=0, blank=True)
    fiftyDayAverage = models.FloatField(default=0, blank=True)

    payoutRatio = models.FloatField(default=0, blank=True)
    regularMarketOpen = models.FloatField(default=0, blank=True)
    regularMarketDayHigh = models.FloatField(default=0, blank=True)


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailing_user')
    ticker = models.CharField(max_length=10, default='')
    company = models.ForeignKey(StockCompany, on_delete=models.CASCADE, related_name='mailing_company', default='')
    create_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ticker

