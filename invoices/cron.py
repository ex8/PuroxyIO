"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.utils import timezone
from invoices.models import Invoice, InvoiceItem
from services.models import Service
from dateutil.relativedelta import relativedelta
from interface.email import SendEmail
from interface.models import Cron
from services.whm import WHM
from django.conf import settings
from django.db.models import Q
from orders.models import Order


def invoice_cron():
    """
    Purpose: Invoices CronJob script
             Further configuration can be found in puroxyio/settings.py
             Used WHMCS Billing Logic as described here: https://docs.whmcs.com/Billing_Logic
             Only generation and suspension, reminder event is yet to be implemented
             Additional documentation is found line by line
    """
    # Define now and results dict
    now = timezone.now()
    results = {
        'generated': 0,
        'reminded': 0,
        'suspended': 0,
        'invoices': []
    }
    # Only work with active and pending service object(s)
    services = Service.objects.filter(
        Q(order__status='active') |
        Q(order__status='pending')
        # Q(order__status='suspended')
    )
    for service in services:
        # Invoice generation
        # First check if service and now are <= 10 days away
        # Then check if an invoice with same invoice.due_date as service.next_due_date
        # if so you know the next_due_date invoice has been created, else you can create the generated invoice
        # If you generate, increment service.next_due_date one (1) month
        order = Order.objects.get(service=service)
        if (service.next_due_date.date() - now.date()).days <= 10:
            # Invoice renewal
            if not Invoice.objects.filter(due_date=service.next_due_date, order=order).exists():
                past_invoice = Invoice.objects.filter(order=order).latest('created')
                generated = generate(
                    now=now,
                    invoice=past_invoice,
                    due_date=service.next_due_date,
                    order=order,
                    service=service
                )
                results['generated'] += 1
                results['invoices'].append(generated)
        # Invoice suspension
        # First check if the date is equal to or less than the number of days in the future
        # If true, then suspend service
        invoice = Invoice.objects.filter(order=order).latest('created')
        if (service.next_due_date.date() - now.date()).days <= -1 and not invoice.paid and not invoice.is_first:
            suspended = suspend(
                invoice=invoice,
                order=order,
                product_type=order.product.type
            )
            results['suspended'] += 1
            results['invoices'].append(suspended)
    Cron.objects.create(results=results)
    SendEmail(
        subject='CronJob Success',
        data={'results': str(results)},
        template='cron-success'
    ).notify_admins()


def generate(now, invoice, due_date, order, service):
    generated = Invoice.objects.create(
        date=now,
        due_date=due_date,
        order=order,
        user=order.user
    )
    for item in invoice.items.all():
        if item.cycle == 'monthly':
            InvoiceItem.objects.create(
                description=item.description,
                amount=item.amount,
                cycle='monthly',
                invoice=generated
            )
    service.next_due_date += relativedelta(months=+1)
    service.save()
    data = {
        'first_name': generated.user.first_name,
        'invoice_id': str(generated.uuid),
        'invoice_date': generated.date.strftime('%m/%d/%y'),
        'invoice_due_date': generated.due_date.strftime('%m/%d/%y'),
        'amount': str(generated.get_total_cost()),
        'product': generated.order.product.name,
        'service': generated.order.service.hostname,
        'status': generated.paid,
    }
    SendEmail(
        subject='Invoice',
        to_email=generated.user.email,
        data=data,
        template='invoice-email',
        user=generated.user
    ).send()
    return generated


def remind(invoice, days_left):
    data = {
        'first_name': invoice.user.first_name,
        'invoice_id': str(invoice.uuid),
        'invoice_date': invoice.date.strftime('%m/%d/%y'),
        'invoice_due_date': invoice.due_date.strftime('%m/%d/%y'),
        'amount': invoice.get_total_cost(),
        'product': invoice.order.product.name,
        'service': invoice.order.service.hostname,
        'status': invoice.paid,
        'days_left': days_left
    }
    SendEmail(
        subject='Invoice Reminder',
        to_email=invoice.user.email,
        data=data,
        template='invoice-reminder-email',
        user=invoice.user
    ).send()
    return invoice


def suspend(invoice, order, product_type):
    InvoiceItem.objects.create(
        description='Late Fee',
        amount=5.00,
        cycle='once',
        invoice=invoice
    )
    if product_type == 'web':
        whm = WHM(
            url=settings.WEB_HOST_BASE_URL,
            username=settings.WEB_HOST_USERNAME,
            password=settings.WEB_HOST_PASSWORD
        )
        whm.suspend(
            username=order.service.username,
            reason='Invoice payment overdue'
        )
    order.status = 'suspended'
    order.save()
    data = {
        'first_name': invoice.user.first_name,
        'product': order.product.name,
        'service': order.service.hostname,
        'reason': 'Invoice payment overdue'
    }
    SendEmail(
        subject='Service Suspension Notification',
        to_email=invoice.user.email,
        data=data,
        template='suspension-email',
        user=invoice.user
    ).send()
    return invoice
