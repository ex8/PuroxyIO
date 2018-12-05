"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from rest_framework import serializers
from invoices.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Purpose: Create Invoice JSON serializer
    """
    order = serializers.ReadOnlyField(source='order.product.name')

    class Meta:
        """
        Purpose: Meta class used in DRF ModelSerializer class
        """
        model = Invoice
        fields = (
            'date', 'due_date', 'paid', 'is_first', 'created', 'order'
        )
