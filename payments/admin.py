"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from payments.models import PaymentGateway, Transaction


class PaymentGatewayAdmin(admin.ModelAdmin):
    """
    Purpose: Generate PaymentGateway admin pages
    """
    list_display = ('name', 'slug', 'available', 'sort', 'color', 'icon')
    list_editable = ('available', 'sort')
    prepopulated_fields = {'slug': ('name',)}


class TransactionAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Transaction admin pages
    """
    list_display = ('uuid', 'txn_id', 'created', 'updated', 'invoice')


# Register model and admin classes
admin.site.register(model_or_iterable=PaymentGateway, admin_class=PaymentGatewayAdmin)
admin.site.register(model_or_iterable=Transaction, admin_class=TransactionAdmin)
