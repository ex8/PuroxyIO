"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
import uuid
from products.models import Product, ProductAddOn
from django.conf import settings
from services.models import Service

# Order status types
STATUS_TYPES = (
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('suspended', 'Suspended'),
    ('cancelled', 'Cancelled'),
    ('terminated', 'Terminated')
)


class Order(models.Model):
    """
    Purpose: Order Model used to document orders
    @uuid: universally unique identifier
    @status: order status type
    @delivered: boolean showing if order is delivered
    @created: order creation date, set automatically
    @updated: last time order was saved, set automatically
    @service: service FK
    @product: product FK
    @addons: addons M-T-M FK
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    status = models.CharField(choices=STATUS_TYPES, max_length=20)
    delivered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    addons = models.ManyToManyField(ProductAddOn)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.service.hostname

    def get_order_status_label(self):
        """
        Purpose: Retrieve order status label
        :return: status dict
        """
        if self.status == 'active':
            s = {
                'label': 'green',
                'status': 'ACTIVE'
            }
        elif self.status == 'pending':
            s = {
                'label': 'yellow',
                'status': 'PENDING'
            }
        elif self.status == 'cancelled':
            s = {
                'label': 'blue',
                'status': 'CANCELLED'
            }
        elif self.status == 'suspended':
            s = {
                'label': 'gray',
                'status': 'SUSPENDED'
            }
        elif self.status == 'terminated':
            s = {
                'label': 'gray',
                'status': 'TERMINATED'
            }
        else:
            s = {
                'label': 'red',
                'status': 'ERROR'
            }
        return s
