# each app has its own urls.py which we will
# connect to assignment_core/urls.py

from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
]