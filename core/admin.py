from django.contrib import admin

# Register your models here.

from django.contrib import admin
from . import models
# Register your models here.


class ProductSite(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name', )
    prepopulated_fields = ({'slug': ('name',)})


class CustomerSite(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name', )
    prepopulated_fields = ({'slug': ('name',)})


class OrderSite(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('id', )



admin.site.register(models.Product, ProductSite)
admin.site.register(models.Customer, CustomerSite)
admin.site.register(models.Order, OrderSite)