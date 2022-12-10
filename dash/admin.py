from django.contrib import admin
from .models import Question
from django import forms

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question)