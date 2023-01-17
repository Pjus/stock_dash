from django.contrib import admin
from .models import FinEventDate, FinancialEvent, FinNews, Currency, StockCompany, CompanyPrice
from django import forms

# Register your models here.
class FinEventDateAdmin(admin.ModelAdmin):
    search_fields = ['fin_current_date']

# Register your models here.
class FinancialEventAdmin(admin.ModelAdmin):
    search_fields = ['event_subject']

class FinNewsAdmin(admin.ModelAdmin):
    search_fields = ['press', 'title']

class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ['country', 'in_korean']

class StockCompanyAdmin(admin.ModelAdmin):
    search_fields = ['ticker', 'company_name']

class CompanyPriceAdmin(admin.ModelAdmin):
    search_fields = ['ticker', 'close_price']


admin.site.register(Currency)
admin.site.register(StockCompany)
admin.site.register(CompanyPrice)


admin.site.register(FinNews)
admin.site.register(FinEventDate)
admin.site.register(FinancialEvent)