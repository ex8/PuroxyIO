"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from rest_framework import serializers
from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    Purpose: Create Invoice JSON serializer
    """
    class Meta:
        """
        Purpose: Meta class used in DRF ModelSerializer class
        """
        model = Service
        fields = (
            'hostname', 'username', 'ip_address', 'os', 'control_panel', 'install_control_panel',
            'additional_ips', 'additional_ips_list', 'created', 'next_due_date'
        )
