from django.urls import path

from .views import base_views, heatmap_view

app_name = 'analysis'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('refresh/', base_views.refresh, name='refresh'),
    path('company/', base_views.company, name='company'),
    path('heatmap/', heatmap_view.get_heatmap, name='heatmap'),

]