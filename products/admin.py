"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from products.models import Product, ProductAddOn, ProductConfiguration, ProductConfigurationOption, \
    ProductConfigurationOptionItem


class ProductAddOnInline(admin.TabularInline):
    """
    Purpose: Tabular inline ProductAddOn used inline with ProductAdmin
    """
    model = ProductAddOn.product.through
    extra = 0


class ProductConfigurationOptionInline(admin.TabularInline):
    """
    Purpose: Tabular inline ProductConfigurationOption used inline with ProductConfigurationAdmin
    """
    model = ProductConfigurationOption
    extra = 0


class ProductConfigurationOptionItemInline(admin.TabularInline):
    """
    Purpose: Tabular inline ProductConfigurationOptionItem used inline with ProductConfigurationOptionAdmin
    """
    model = ProductConfigurationOptionItem
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Product admin pages
    """
    list_display = ('name', 'slug', 'type', 'available', 'price')
    list_filter = ('type', 'available')
    list_editable = ('price', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAddOnInline]


class ProductAddOnAdmin(admin.ModelAdmin):
    """
    Purpose: Generate ProductAddOn admin pages
    """
    list_display = ('name', 'description', 'price', 'available')
    list_filter = ('available',)
    list_editable = ('price', 'available')
    search_fields = ('name', 'description')


class ProductConfigurationAdmin(admin.ModelAdmin):
    """
    Purpose: Generate ProductConfiguration admin pages
    """
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [ProductConfigurationOptionInline]


class ProductConfigurationOptionAdmin(admin.ModelAdmin):
    """
    Purpose: Generate ProductConfigurationOption admin pages
    """
    list_display = ('name', 'type', 'sort', 'available', 'configuration')
    list_filter = ('type',)
    list_editable = ('available', 'sort')
    search_fields = ('name',)
    inlines = [ProductConfigurationOptionItemInline]


# Register model and admin classes
admin.site.register(model_or_iterable=Product, admin_class=ProductAdmin)
admin.site.register(model_or_iterable=ProductAddOn, admin_class=ProductAddOnAdmin)
admin.site.register(model_or_iterable=ProductConfiguration, admin_class=ProductConfigurationAdmin)
admin.site.register(model_or_iterable=ProductConfigurationOption, admin_class=ProductConfigurationOptionAdmin)
