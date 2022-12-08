from django.urls import path

from .views import base_views

app_name = 'analysis'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('company/', base_views.company, name='company'),

]