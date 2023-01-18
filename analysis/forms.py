from django import forms
from .models import MailingTicker

class MailingForm(forms.ModelForm):
    class Meta:
        model = MailingTicker
        fields = ['ticker']  