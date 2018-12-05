"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
import uuid
from django.conf import settings


class Service(models.Model):
    """
    Purpose: Service Model used to document services
    @uuid: universally unique identifier
    @hostname: domain or server hostname (used for mainly client)
    @username: service username
    @password: service password
    @ip_address: main service IP address
    @os: operating system
    @control_panel: service control panel (if any)
    @install_control_panel: license or license & install control panel ? (boolean)
    @additional_ips: number of additional IP's
    @additional_ips_list: list of additional IP's, separated by newline (\n)
    @api_key: API key used to handle server operations (reboot, boot, shutdown, etc), must have api_hash set
    @api_hash: API hash used to handle server operations, must api_key set
    @created: service creation date, set automatically
    @updated: last datetime service was saved, set automatically
    @next_due_date: next billing due date cycle (used in cron)
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    hostname = models.CharField(unique=True, max_length=50)
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    os = models.CharField(max_length=50)
    control_panel = models.CharField(max_length=50)
    install_control_panel = models.CharField(max_length=50)
    additional_ips = models.PositiveIntegerField()
    additional_ips_list = models.TextField(blank=True)
    api_key = models.CharField(max_length=250, blank=True)
    api_hash = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    next_due_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.hostname
