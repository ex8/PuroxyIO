"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
import uuid
from invoices.models import Invoice


class PaymentGateway(models.Model):
    """
    Purpose: Payment Gateway Model used to document payment processing gateways
    @name: gateway name
    @slug: gateway slug used for URL, pre-populated from @name
    @post_url: url to POST payment data to
    @description: payment gateway description
    @color: hexcode color for icon-box stack
    @icon: font-awesome icon code for icon-box stack
    @sort: integer field for gateway sort filter
    @available: is gateway available ?
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    post_url = models.CharField(max_length=150)
    description = models.TextField()
    color = models.CharField(max_length=10)
    icon = models.CharField(max_length=25)
    sort = models.PositiveIntegerField()
    available = models.BooleanField(default=False)

    class Meta:
        """
        Purpose: Meta class used for Django Model class and Django Admin
        """
        ordering = ('sort',)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Purpose: Transaction Model used to document payment actions
    @uuid: universally unique identifier
    @txn_id: transaction id from POST response
    @created: creation date, set automatically
    @updated: last time transaction was saved, set automatically
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    txn_id = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    invoice = models.ForeignKey(Invoice)
