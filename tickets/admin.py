"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from tickets.models import Ticket, Response


class ResponseInline(admin.TabularInline):
    """
    Purpose: Tabular inline TicketResponse used inline with TicketAdmin found below
    """
    model = Response
    fields = ('message', 'user')
    raw_id_fields = ('user',)
    ordering = ['-created']
    extra = 1


class TicketAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Ticket admin pages
    """
    list_display = ('user', 'subject', 'message', 'status', 'priority', 'service')
    list_filter = ('status', 'priority')
    search_fields = ('subject', 'message')
    raw_id_fields = ('user',)
    inlines = [ResponseInline]


# Register model and admin class
admin.site.register(model_or_iterable=Ticket, admin_class=TicketAdmin)
