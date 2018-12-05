"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from services.models import Service
from django.conf import settings
import random
import string


def create_service(product_type, data, next_due_date, user):
    """
    Purpose: Create service object from new order
    :param product_type: type of product
    :param data: POST data from newly created order
    :param next_due_date: service next_due_date field
    :param user: user FK
    :return: service
    """
    if product_type == 'web':
        service = Service.objects.create(
            hostname=data['Domain (example.com)'],
            os=settings.WEB_HOST_OPERATING_SYSTEM,
            control_panel=settings.WEB_HOST_CONTROL_PANEL,
            install_control_panel='NO',
            additional_ips=0,
            next_due_date=next_due_date,
            user=user
        )
        return service
    elif product_type == 'linux_vps' or product_type == 'onshore_dedicated':
        service = Service.objects.create(
            hostname=data['Hostname'],
            os=data['Operating System'],
            control_panel=data['Control Panel'],
            install_control_panel=data['Install Control Panel?'],
            additional_ips=int(data['Additional IP Addresses'].split()[0]),
            next_due_date=next_due_date,
            user=user
        )
        return service
    elif product_type == 'window_vps':
        service = Service.objects.create(
            hostname=data['Hostname'],
            os=data['Operating System'],
            additional_ips=int(data['Additional IP Addresses'].split()[0]),
            next_due_date=next_due_date,
            user=user
        )
        return service
    elif product_type == 'offshore_dedicated':
        service = Service.objects.create(
            hostname=data['Hostname'],
            os=data['Operating System'],
            additional_ips=0,
            next_due_date=next_due_date,
            user=user
        )
        return service


def generate_username():
    """
    Purpose: Generate random 8 character username
    :return: string
    """
    return ''.join(random.choice(string.ascii_lowercase) for i in range(8))


def generate_password():
    """
    Purpose: Generate random 16 character username
    :return: string
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join((random.choice(chars)) for i in range(16))
