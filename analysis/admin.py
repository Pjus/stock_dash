from django.contrib import admin
from .models import FinEventDate, FinancialEvent, FinNews
from django import forms

# Register your models here.
class FinEventDateAdmin(admin.ModelAdmin):
    search_fields = ['fin_current_date']

# Register your models here.
class FinancialEventAdmin(admin.ModelAdmin):
    search_fields = ['event_subject']

class FinNewsAdmin(admin.ModelAdmin):
    search_fields = ['press', 'title']

admin.site.register(FinNews)
admin.site.register(FinEventDate)
admin.site.register(FinancialEvent)