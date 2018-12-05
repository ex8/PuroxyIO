"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
from django.conf import settings
import uuid


class API(models.Model):
    """
    Purpose: API Model used for keeping records of incoming requests
    @uuid: universally uniquely identifier
    @date_requested: incoming request date, automatically set
    @completed: is incoming request complete ?
    @data: requested json data
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date_requested = models.DateTimeField(auto_now_add=True)
    endpoint_name = models.CharField(max_length=100)
    completed = models.BooleanField()
    data = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        """
        Purpose: Meta data for initial QuerySet loaded in admin (mostly used by Django-Admin)
        """
        ordering = ('-date_requested',)
        verbose_name = 'API'

    def __str__(self):
        return self.endpoint_name
