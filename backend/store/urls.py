from django.urls import path
from .views import home_view, categories_view, contact_view, category_detail_view, products_view

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', categories_view, name='categories'),
    path('contact/', contact_view, name='contact'),
    path('categories/<slug:slug>/', category_detail_view, name='category_detail'),
    path('products/', products_view, name='products')
]