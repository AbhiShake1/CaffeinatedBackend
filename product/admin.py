from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_filter = ('price',)
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)
