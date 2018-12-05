"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from interface.models import Email, Cron


class EmailAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Email admin pages
    """
    list_display = ('subject', 'to_email', 'created', 'user')
    search_fields = ('subject', 'user')


class CronAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Cron admin pages
    """
    list_display = ('date', 'results')
    search_fields = ('results',)


# Set Admin headers
admin.site.site_title = "PuroxyIO"
admin.site.site_header = "PuroxyIO Administration"

# Register model and admin class
admin.site.register(model_or_iterable=Email, admin_class=EmailAdmin)
admin.site.register(model_or_iterable=Cron, admin_class=CronAdmin)
