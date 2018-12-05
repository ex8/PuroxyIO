"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from products.models import Product, ProductAddOn, ProductConfiguration, ProductConfigurationOption
from products.forms import ProductConfigurationForm, ProductAddOnForm
from products.helpers import create_product_configuration_invoice_items, create_product_addon_invoice_items
from orders.models import Order
from invoices.models import Invoice, InvoiceItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from services.helpers import create_service
from interface.email import SendEmail


@login_required
def order_list(request):
    """
    Purpose: Retrieve orders page; which is list of all available products ordered by price
             Ordering can be disabled from puroxyio/settings.py
    :param request: incoming request
    :return: rendered HTML template with products
    """
    if settings.ORDER:
        web = Product.objects.filter(type='web', available=True).order_by('price')
        linux_vps = Product.objects.filter(type='linux_vps', available=True).order_by('price')
        window_vps = Product.objects.filter(type='window_vps', available=True).order_by('price')
        onshore = Product.objects.filter(type='onshore_dedicated', available=True).order_by('price')
        offshore = Product.objects.filter(type='offshore_dedicated', available=True).order_by('price')
        return render(request=request, template_name='orders/list.html', context={
            'web': [(web[i], web[i + 1]) for i in range(0, len(web), 2)],
            'linux_vps': [(linux_vps[i], linux_vps[i + 1]) for i in range(0, len(linux_vps), 2)],
            'window_vps': [(window_vps[i], window_vps[i + 1]) for i in range(0, len(window_vps), 2)],
            'onshore': [(onshore[i], onshore[i + 1]) for i in range(0, len(onshore), 2)],
            'offshore': [(offshore[i], offshore[i + 1]) for i in range(0, len(offshore), 2)]
        })
    return render(request=request, template_name='orders/list.html', context={
        'disabled': True
    })


@login_required
def order_detail(request, slug):
    """
    Purpose: Retrieve order/product detail including respective configuration
             A series of helper functions can be found in `products` app to simplify readability
    :param request: incoming request
    :param slug: beautiful slugged-url, key to product
    :return: rendered HTML template with detailed order/product/configuration
    """
    product = get_object_or_404(klass=Product, slug=slug)
    configuration = ProductConfiguration.objects.get(product=product)
    options = ProductConfigurationOption.objects.filter(configuration=configuration, available=True).order_by('sort')
    addons = ProductAddOn.objects.filter(product=product, available=True).order_by('price')
    if settings.ORDER:
        if request.method == 'POST':
            form = ProductConfigurationForm(data=request.POST, options=options)
            addon_form = ProductAddOnForm(data=request.POST, addons=addons)
            if form.is_valid() and addon_form.is_valid():
                now = timezone.now()
                order = Order.objects.create(
                    status='pending',
                    product=product,
                    user=request.user
                )
                invoice = Invoice.objects.create(
                    date=now,
                    due_date=now,
                    is_first=True,
                    order=order,
                    user=request.user
                )
                InvoiceItem.objects.create(
                    description=product.description,
                    amount=product.price,
                    cycle='monthly',
                    invoice=invoice
                )
                create_product_configuration_invoice_items(
                    product_type=product.type,
                    data=form.cleaned_data,
                    invoice=invoice
                )
                create_product_addon_invoice_items(
                    data=addon_form.cleaned_data,
                    order=order,
                    invoice=invoice
                )
                service = create_service(
                    product_type=product.type,
                    data=form.cleaned_data,
                    next_due_date=now,
                    user=request.user
                )
                order.service = service
                order.save()

                order_email_data = {
                    'first_name': request.user.first_name,
                    'order_id': str(order.uuid),
                    'product': order.product.name,
                    'hostname': service.hostname
                }
                SendEmail(
                    subject='PuroxyIO Order Confirmation',
                    to_email=request.user.email,
                    data=order_email_data,
                    template='order-confirm-email',
                    user=request.user
                ).send()
                invoice_email_data = {
                    'first_name': request.user.first_name,
                    'invoice_id': str(invoice.uuid),
                    'invoice_date': invoice.date.strftime('%m/%d/%y'),
                    'invoice_due_date': invoice.due_date.strftime('%m/%d/%y'),
                    'amount': str(invoice.get_total_cost()),
                    'product': order.product.name,
                    'service': service.hostname,
                    'status': invoice.paid
                }
                SendEmail(
                    subject='PuroxyIO Invoice',
                    to_email=request.user.email,
                    data=invoice_email_data,
                    template='invoice-email',
                    user=request.user
                ).send()
                admin_order_email_data = {
                    'client': '{} {}'.format(request.user.first_name, request.user.last_name),
                    'order_id': str(order.uuid),
                    'product': order.product.name,
                    'hostname': service.hostname
                }
                SendEmail(
                    subject='New PuroxyIO Order Notification',
                    data=admin_order_email_data,
                    template='new-order-email',
                ).notify_admins()
                messages.success(request=request, message='Your order was successfully created')
                return HttpResponseRedirect(redirect_to=reverse('invoices:detail', kwargs={
                    'uuid': invoice.uuid
                }))
            else:
                messages.error(request=request, message='Your product configuration was invalid.')
                messages.warning(request=request, message='The hostname may already exist in our system.')
        else:
            form = ProductConfigurationForm(options=options)
            addon_form = ProductAddOnForm(addons=addons)
        return render(request=request, template_name='orders/detail.html', context={
            'product': product,
            'form': form,
            'addon_form': addon_form
        })
    return render(request=request, template_name='orders/detail.html', context={
        'disabled': True
    })
