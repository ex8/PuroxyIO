"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Order admin pages
    """
    list_display = ('service', 'user', 'status', 'delivered', 'created', 'product')
    list_editable = ('delivered', 'status')
    list_filter = ('status', 'delivered')
    search_fields = ('user', 'product')


# Register model and admin class
admin.site.register(model_or_iterable=Order, admin_class=OrderAdmin)
