"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
from orders.models import Order
from django.conf import settings
import uuid

# InvoiceItem item cycle choices; used for cron !
ITEM_CYCLES = (
    ('once', 'Once'),
    ('monthly', 'Monthly')
)


class Invoice(models.Model):
    """
    Purpose: Invoice Model used to document invoices
    @uuid: universally unique identifier
    @date: invoice created date (similar to `created`)
    @due_date: invoice due_date
    @paid: boolean to show if invoice is paid
    @date_paid: dating when invoice was paid, default is null
    @method: payment method used; as of now: BCH, BTC, ETH, DASH, PP
    @is_first: is this the first invoice of the sequence
    @created: invoice created date
    @updated: last datetime invoice was saved
    @order: every invoice is associated to an order (thus a service invoice->order->service)
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    date = models.DateTimeField()
    due_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=50, blank=True)
    is_first = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Invoice #{} for Order: {}'.format(self.id, self.order.service.hostname)

    def get_total_cost(self):
        """
        Purpose: Get the total amount cost for invoice
        :return: sum of all invoice items (using related_name=`items`)
        """
        if self.items.exists():
            return sum(i.amount for i in self.items.all())
        return 0


class InvoiceItem(models.Model):
    """
    Purpose: InvoiceItem Model used to document items associated to an Invoice
    @description: invoice item description
    @amount: amount invoice item costs
    @cycle: item cycle (once, monthly)
    @invoice: invoice FK
    """
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    cycle = models.CharField(choices=ITEM_CYCLES, max_length=20)
    invoice = models.ForeignKey(Invoice, related_name='items')

    def __str__(self):
        return 'InvoiceItem for Invoice #{}'.format(self.invoice.id)
