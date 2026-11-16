from django.urls import path
from .views import home_view, categories_view, contact_view, category_detail_view, products_view, product_detail_view, cart_add,cart_remove,cart_update,cart_view

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', categories_view, name='categories'),
    path('contact/', contact_view, name='contact'),
    path('categories/<slug:slug>/', category_detail_view, name='category_detail'),
    path('products/', products_view, name='products'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:pk>/', cart_add, name='cart_add'),
    path('cart/update/<int:pk>', cart_update, name="cart_update"),
    path('cart/remove/<int:pk>', cart_remove, name="cart_remove"),
]