"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from invoices.models import InvoiceItem
from products.models import ProductAddOn, ProductConfigurationOptionItem


def create_product_configuration_invoice_items(product_type, data, invoice):
    """
    Purpose: Create ProductConfiguration InvoiceItems based on Config from new order
    :param product_type: product type choice from Model
    :param data: POST data from new order
    :param invoice: invoice object to work with (attaching InvoiceItems to)
    :return: items
    """
    items = []
    if product_type == 'linux_vps' or product_type == 'onshore_dedicated':
        ip = data['Additional IP Addresses']
        cp = data['Control Panel']
        ips = int(ip.split()[0])
        if not (ips == 0):
            option_item = ProductConfigurationOptionItem.objects.filter(name=ip)[0]
            item = InvoiceItem.objects.create(
                description='{} - {}'.format(option_item.name, ips),
                amount=option_item.price,
                cycle='monthly',
                invoice=invoice
            )
            items.append(item)
        if 'Not applicable (N/A)' not in cp:
            option_item = ProductConfigurationOptionItem.objects.get(name=cp)
            item = InvoiceItem.objects.create(
                description=option_item.name,
                amount=option_item.price,
                cycle='monthly',
                invoice=invoice
            )
            items.append(item)
    elif product_type == 'window_vps':
        ip = data['Additional IP Addresses']
        ips = int(ip.split()[0])
        if not (ips == 0):
            option_item = ProductConfigurationOptionItem.objects.filter(name=ip)[0]
            item = InvoiceItem.objects.create(
                description='{} - {}'.format(option_item.name, ips),
                amount=option_item.price,
                cycle='monthly',
                invoice=invoice
            )
            items.append(item)
    return items


def create_product_addon_invoice_items(data, order, invoice):
    """
    Purpose: Create ProductAddOn InvoiceItems from new order
    :param data: POST data from new order
    :param order: newly created order object
    :param invoice: invoice object to work with (attaching InvoiceItems to)
    :return: items
    """
    items = []
    for k, v in data.items():
        if v == 'True':
            addon = ProductAddOn.objects.get(name=k)
            item = InvoiceItem.objects.create(
                description=addon.name,
                amount=addon.price,
                cycle='once',
                invoice=invoice
            )
            order.addons.add(addon)
            items.append(item)
    return items
