from django.db import models



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