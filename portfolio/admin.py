from django.contrib import admin
from .models import Portfolio, Stock, Transaction

# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    search_fields = ['title']


class StockAdmin(admin.ModelAdmin):
    search_fields = ['ticker', 'add_port']

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['ticker', 'trans_portfolio']


admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(Transaction)

