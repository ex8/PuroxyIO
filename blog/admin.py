"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    """
    Purpose: Generate Blog admin pages
    """
    list_display = ('title', 'published', 'updated', 'user')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    raw_id_fields = ('user',)


# Register model and admin class
admin.site.register(model_or_iterable=Post, admin_class=PostAdmin)
