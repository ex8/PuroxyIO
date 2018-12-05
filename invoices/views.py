"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, get_object_or_404
from invoices.models import Invoice
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def invoice_list(request):
    """
    Purpose: Retrieve invoice(s) associated to user
    :param request: incoming request
    :return: rendered HTML template with invoices
    """
    objects = Invoice.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(object_list=objects, per_page=10)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(number=page)
    except PageNotAnInteger:
        invoices = paginator.page(number=1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    return render(request=request, template_name='invoices/list.html', context={
        'invoices': invoices
    })


@login_required
def invoice_detail(request, uuid):
    """
    Purpose: Retrieve invoice detail associated to user
    :param request: incoming request
    :param uuid: invoice universally unique identifier
    :return: rendered HTML template with detailed invoice
    """
    invoice = get_object_or_404(klass=Invoice, uuid=uuid, user=request.user)
    return render(request=request, template_name='invoices/detail.html', context={
        'invoice': invoice,
    })
