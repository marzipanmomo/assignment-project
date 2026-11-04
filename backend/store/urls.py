from django.urls import path
from .views import home_view, categories_view, contact_view

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', categories_view, name='categories'),
    path('contact/', contact_view, name='contact'),
]