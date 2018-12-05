"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings


class Email(models.Model):
    """
    Purpose: Email Model used to document emails
    @subject: email subject
    @to_email: receiver's email
    @from_email: sender's email
    @from_name: sender's name
    @body: email body
    @created: email creation date, automatically set
    @user: user FK
    """
    subject = models.CharField(max_length=100)
    to_email = models.EmailField()
    from_email = models.EmailField()
    from_name = models.CharField(max_length=100)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')

    def __str__(self):
        return self.subject


class Cron(models.Model):
    """
    Purpose: Cron Model used to document cronjobs
    @date: cron run datetime, automatically set
    @results: results dict
    """
    date = models.DateTimeField(auto_now_add=True)
    results = models.TextField()

    class Meta:
        """
        Purpose: Meta data for initial QuerySet loaded in admin (mostly used by Django-Admin)
        """
        verbose_name = 'Cron Job'
        verbose_name_plural = 'Cron Jobs'

    def __str__(self):
        return 'Cron Job #{}'.format(self.id)
