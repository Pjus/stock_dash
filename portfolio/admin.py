from django.contrib import admin
from .models import Portfolio, Stock

# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    search_fields = ['title']


class StockAdmin(admin.ModelAdmin):
    search_fields = ['ticker', 'add_port']

admin.site.register(Portfolio)
admin.site.register(Stock)
