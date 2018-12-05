"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField


class Post(models.Model):
    """
    Purpose: Post Model used to store a collection of blog posts
            Used at {base_url}/blog
    @title: title of blog post (main subject)
    @slug: beautiful slug URL, pre-populated from @title
    @body: rich body text for main blog content (can use HTML)
    @published: is blog post published to the world ?
    @created: blog post creation date, automatically set
    @updated: last updated blog post date, automatically set/updated
    @user: user FK
    """
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True)
    body = RichTextField()
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        """
        Purpose: Meta data for initial QuerySet loaded in admin (mostly used by Django-Admin)
        """
        ordering = ('-created',)

    def __str__(self):
        return self.title
