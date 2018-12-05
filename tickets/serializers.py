"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from rest_framework import serializers
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Purpose: Create Ticket JSON serializer
    """
    class Meta:
        """
        Purpose: Meta class used in DRF ModelSerializer class
        """
        model = Ticket
        fields = (
            'subject', 'message', 'status', 'priority', 'created'
        )
