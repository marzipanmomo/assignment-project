from django.contrib import admin
from .models import Category, Product, ContactMessage

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'slug')
    list_filter = ('group',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_featured')
    list_filter = ('is_featured', 'categories__group')
    search_fields = ('name',)
    filter_horizontal = ('categories',)

admin.site.register(ContactMessage)