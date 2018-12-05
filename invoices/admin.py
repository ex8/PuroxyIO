"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from invoices.models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    """
    Purpose: Tabular inline InvoiceItem used inline with InvoiceAdmin found below
    """
    model = InvoiceItem
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Invoice admin pages
    """
    list_display = ('order', 'date', 'due_date', 'paid', 'method', 'user')
    list_editable = ('paid',)
    list_filter = ('paid', 'is_first')
    search_fields = ('user', 'order')
    raw_id_fields = ('user',)
    inlines = [InvoiceItemInline]


# Register model and admin class
admin.site.register(model_or_iterable=Invoice, admin_class=InvoiceAdmin)
