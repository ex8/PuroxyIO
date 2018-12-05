"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from payments.models import PaymentGateway, Transaction
from invoices.models import Invoice
from django.contrib.auth.decorators import login_required
from payments.forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.utils.http import urlencode
from django.conf import settings
from django.utils import timezone
from services.whm import WHM
from decimal import Decimal
from services.helpers import generate_password, generate_username
from interface.email import SendEmail
from dateutil.relativedelta import relativedelta
import hashlib
import logging
import hmac


@login_required
def gateway_list(request, uuid):
    """
    Purpose: Retrieve Payment Gateway objects available
    :param request: incoming request
    :param uuid: university unique identifier key to invoice
    :return: rendered HTML template with invoice and available gateways
    """
    invoice = get_object_or_404(klass=Invoice, uuid=uuid, user=request.user)
    if invoice.paid:
        return HttpResponseRedirect(reverse('invoices:detail', kwargs={
            'uuid': invoice.uuid
        }))
    gateways = PaymentGateway.objects.filter(available=True)[:4]
    return render(request=request, template_name='payments/list.html', context={
        'invoice': invoice,
        'gateways': gateways
    })


@login_required
def process(request, uuid, slug):
    """
    Purpose: Process payment gateway, send POST request using PaymentForm
    :param request: incoming request
    :param uuid: universally unique identifier key to invoice
    :param slug: beautiful slug key for gateway
    :return: rendered HTML template with invoice, detailed gateway, and hidden form
    """
    invoice = get_object_or_404(klass=Invoice, uuid=uuid, user=request.user)
    if invoice.paid:
        return HttpResponseRedirect(reverse('invoices:detail', kwargs={
            'uuid': invoice.uuid
        }))
    gateway = get_object_or_404(klass=PaymentGateway, slug=slug)
    form = PaymentForm(initial={
        'cmd': '_pay_simple',
        'reset': '1',
        'merchant': settings.COINPAYMENTS_MERCHANT_ID,
        'currency': 'USD',
        'amountf': invoice.get_total_cost(),
        'item_name': invoice.order.product.name,
        'invoice': invoice.uuid,
        'allow_currencies': 'Paypal,BTC,BCH,ETH,DASH',
        'ipn_url': '{}://{}{}'.format(
            request.is_secure() and 'https' or 'http',
            request.get_host(),
            reverse('payments:ipn')
        ),
        'success_url': '{}://{}{}'.format(
            request.is_secure() and 'https' or 'http',
            request.get_host(),
            reverse('payments:success', kwargs={
                'uuid': invoice.uuid,
                'slug': gateway.slug
            })
        ),
        'cancel_url': '{}://{}{}'.format(
            request.is_secure() and 'https' or 'http',
            request.get_host(),
            reverse('payments:cancelled', kwargs={
                'uuid': invoice.uuid,
                'slug': gateway.slug
            })
        ),
        'first_name': invoice.user.first_name,
        'last_name': invoice.user.last_name,
        'email': invoice.user.email,
    })
    return render(request=request, template_name='payments/process.html', context={
        'invoice': invoice,
        'gateway': gateway,
        'form': form
    })


@csrf_exempt
@login_required
def success(request, uuid, slug):
    """
    Purpose: Payment gateway processing success, using CSRF_exempt so route can receive POST from IPN
    :param request: incoming request
    :param uuid: universally unique identifier key to invoice
    :param slug: beautiful slug key for gateway
    :return: rendered HTML template with invoice & detailed gateway
    """
    invoice = get_object_or_404(klass=Invoice, uuid=uuid, user=request.user)
    gateway = get_object_or_404(klass=PaymentGateway, slug=slug)
    return render(request=request, template_name='payments/success.html', context={
        'invoice': invoice,
        'gateway': gateway
    })


@csrf_exempt
@login_required
def cancelled(request, uuid, slug):
    """
        Purpose: Payment gateway processing cancelled, using CSRF_exempt so route can receive POST from IPN
        :param request: incoming request
        :param uuid: universally unique identifier key to invoice
        :param slug: beautiful slug key for gateway
        :return: rendered HTML template with invoice & detailed gateway
        """
    invoice = get_object_or_404(klass=Invoice, uuid=uuid, user=request.user)
    if invoice.paid:
        return HttpResponseRedirect(reverse('invoices:detail', kwargs={
            'uuid': invoice.uuid
        }))
    gateway = get_object_or_404(klass=PaymentGateway, slug=slug)
    return render(request=request, template_name='payments/cancelled.html', context={
        'invoice': invoice,
        'gateway': gateway
    })


@csrf_exempt
def ipn(request):
    """
    Purpose: Instant Payment Notification (IPN) listener
    :param request: incoming request
    :return: HTTPResponse
    """
    data = request.POST
    if data:
        invoice_uuid = data['invoice']
        if not invoice_uuid:
            return HttpResponseBadRequest('No invoice uuid')
        try:
            invoice = Invoice.objects.get(uuid=invoice_uuid)
        except Invoice.DoesNotExist:
            return HttpResponseBadRequest('IPN invoice does not exist.')
        status = int(data['status'])
        if status < 0:
            SendEmail(
                subject='Payment Error',
                data={
                    'invoice_id': str(invoice.uuid)
                },
                template='payment-error'
            ).notify_admins()
            return HttpResponse()
        elif 0 <= status <= 99:
            return HttpResponse()
        elif status >= 100:
            post_hmac = request.META['HTTP_HMAC']
            if not post_hmac:
                return HttpResponseBadRequest('No HMAC sent.')
            local_hmac = hmac.new(
                key=bytearray(settings.COINPAYMENTS_IPN_SECRET, 'utf-8'),
                msg=urlencode(request).encode('utf-8'),
                digestmod=hashlib.sha512
            ).hexdigest()
            if local_hmac != post_hmac:
                return HttpResponseBadRequest('IPN request from unapproved gateway.')
            merchant = data['merchant']
            if not merchant:
                return HttpResponseBadRequest('No merchant ID sent.')
            if merchant != settings.COINPAYMENTS_MERCHANT_ID:
                return HttpResponseBadRequest('Incorrect merchant ID.')
            amount = data['amount1']
            if Decimal(amount) != invoice.get_total_cost():
                return HttpResponseBadRequest('Incorrect invoice amount.')

            Transaction.objects.create(txn_id=data['txn_id'], invoice=invoice)
            invoice.paid = True
            invoice.date_paid = timezone.now()
            invoice.method = data['currency2']
            invoice.save()
            service = invoice.order.service
            service.save()
            invoice_confirm_email_data = {
                'first_name': invoice.user.first_name,
                'invoice_date': invoice.date.strftime('%m/%d/%y'),
                'invoice_due_date': invoice.due_date.strftime('%m/%d/%y'),
                'amount': str(invoice.get_total_cost()),
                'product': invoice.order.product.name,
                'service': invoice.order.service.hostname,
                'status': invoice.paid,
                'date_paid': invoice.date_paid.strftime('%m/%d/%y'),
                'txn_id': data['txn_id'],
                'invoice_id': str(invoice.uuid)
            }
            SendEmail(
                subject='Payment Confirmation',
                to_email=invoice.user.email,
                data=invoice_confirm_email_data,
                template='invoice-confirm-email',
                user=invoice.user
            ).send()
            if invoice.is_first and invoice.order.product.type == 'web':
                whm = WHM(
                    url=settings.WEB_HOST_BASE_URL,
                    username=settings.WEB_HOST_USERNAME,
                    password=settings.WEB_HOST_PASSWORD
                )
                service = invoice.order.service
                order = invoice.order
                username = generate_username()
                password = generate_password()
                whm.create(
                    username=username, password=password,
                    domain=order.service.hostname,
                    plan=order.product.whm_package
                )
                service.ip_address = settings.WEB_HOST_MAIN_IP
                service.username = username
                service.next_due_date += relativedelta(months=+1)
                service.save()
                order.status = 'active'
                order.delivered = True
                order.save()
                cpanel_account_email_data = {
                    'first_name': invoice.user.first_name,
                    'product': order.product.name,
                    'hostname': service.hostname,
                    'cpanel_user': username,
                    'cpanel_password': password,
                    'service_id': str(service.uuid)
                }
                admin_email_data = {
                    'client': '{} {}'.format(invoice.user.first_name, invoice.user.last_name),
                    'order_id': str(invoice.order.uuid),
                    'product': service.product.name,
                    'hostname': service.hostname
                }
                SendEmail(
                    subject='cPanel Account Information',
                    to_email=invoice.user.email,
                    data=cpanel_account_email_data,
                    template='cpanel-account-info',
                    user=invoice.user
                ).send()
                SendEmail(
                    subject='cPanel Account Creation Success',
                    data=admin_email_data,
                    template='cpanel-success-admin',
                ).notify_admins()
            if invoice.order.status == 'suspended' and invoice.order.product.type == 'web':
                whm = WHM(
                    url=settings.WEB_HOST_BASE_URL,
                    username=settings.WEB_HOST_USERNAME,
                    password=settings.WEB_HOST_PASSWORD
                )
                order = invoice.order
                service = order.service
                whm.unsuspend(username=order.service.username)
                order.status = 'active'
                order.save()
                unsuspend_cpanel_email_data = {
                    'first_name': invoice.user.first_name,
                    'product': service.product.name,
                    'hostname': service.hostname,
                    'amount': str(invoice.get_total_cost()),
                    'due_date': invoice.due_date.strftime('%m/%d/%y'),
                    'service_id': str(service.uuid)
                }
                unsuspend_cpanel_admin_success_data = {
                    'client': '{} {}'.format(invoice.user.first_name, invoice.user.last_name),
                    'order': str(order.uuid),
                    'product': order.product.name,
                    'hostname': service.hostname,
                }
                SendEmail(
                    subject='Service Un-suspension Notification',
                    to_email=invoice.user,
                    data=unsuspend_cpanel_email_data,
                    template='unsuspend-notification-email',
                    user=invoice.user
                ).send()
                SendEmail(
                    subject='cPanel Account Un-suspend Success',
                    data=unsuspend_cpanel_admin_success_data,
                    template='cpanel-admin-unsuspend-success'
                ).notify_admins()
        return HttpResponse()
