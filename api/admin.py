"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from api.models import API


class APIAdmin(admin.ModelAdmin):
    """
    Purpose: Generate API admin pages
    """
    list_display = ('user', 'date_requested', 'endpoint_name', 'completed')


# Register model and admin class
admin.site.register(model_or_iterable=API, admin_class=APIAdmin)
