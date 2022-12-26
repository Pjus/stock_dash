from django.urls import path
from .views import base_views


app_name = "user"


urlpatterns = [
    path("profile/", base_views.profile, name="profile")
]
