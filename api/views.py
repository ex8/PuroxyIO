"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import API
from services.models import Service
from invoices.models import Invoice
from tickets.models import Ticket
from services.serializers import ServiceSerializer
from invoices.serializers import InvoiceSerializer
from tickets.serializers import TicketSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def api_list(request):
    """
    Purpose: Retrieve API objects for requested user
    :param request: incoming request
    :return: rendered HTML template with apis, total count, successful & failed counts
    """
    objects = API.objects.filter(user=request.user)
    paginator = Paginator(object_list=objects, per_page=10)
    page = request.GET.get('page')
    try:
        apis = paginator.page(number=page)
    except PageNotAnInteger:
        apis = paginator.page(number=1)
    except EmptyPage:
        apis = paginator.page(paginator.num_pages)
    return render(request=request, template_name='api/list.html', context={
        'apis': apis,
        'count': objects.count(),
        'success': objects.filter(completed=True).count(),
        'fail': objects.filter(completed=False).count()
    })


@login_required
def api_detail(request, uuid):
    """
    Purpose: Retrieve detailed API object
    :param request: incoming request
    :param uuid: universally unique identifier
    :return: rendered HTML template with api object(s)
    """
    api = get_object_or_404(klass=API, uuid=uuid, user=request.user)
    return render(request=request, template_name='api/detail.html', context={
        'api': api,
    })


@api_view(['GET'])
def service_list(request, format=None):
    """
    Purpose: Retrieve service object(s) for requested user
    :param request: Incoming request
    :param format: JSON or XML, default JSON (mainly used in DRF)
    :return: JSON response with serialized service data
    """
    services = Service.objects.filter(user=request.user)
    serializer = ServiceSerializer(services, many=True)
    API.objects.create(
        endpoint_name='Service list',
        completed=True,
        data=serializer.data,
        user=request.user
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def invoice_list(request, format=None):
    """
    Purpose: Retrieve invoice object(s) for requested user
    :param request: Incoming request
    :param format: JSON or XML, default JSON (mainly used in DRF)
    :return: JSON response with serialized invoice(s) data
    """
    invoices = Invoice.objects.filter(user=request.user)
    serializer = InvoiceSerializer(invoices, many=True)
    API.objects.create(
        endpoint_name='Invoice list',
        completed=True,
        data=serializer.data,
        user=request.user
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ticket_list(request, format=None):
    """
    Purpose: Retrieve ticket object(s) for requested user
    :param request: Incoming request
    :param format: JSON or XML, default JSON (mainly used in DRF)
    :return: JSON response with serialized ticket(s) data
    """
    tickets = Ticket.objects.filter(user=request.user)
    serializer = TicketSerializer(tickets, many=True)
    API.objects.create(
        endpoint_name='Ticket list',
        completed=True,
        data=serializer.data,
        user=request.user
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
