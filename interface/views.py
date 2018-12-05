"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login, password_reset, password_reset_confirm, password_change
from django.contrib.auth.decorators import login_required
from interface.forms import UserRegisterForm, UserSettingsForm
from orders.models import Order
from invoices.models import Invoice
from django.db.models import Q
from tickets.models import Ticket
from django.contrib import messages
import requests
import requests.exceptions
from api.models import API


@login_required
def dashboard(request):
    """
    Purpose: Main dashboard for interface.
             Use GET request to check main node's status
             Use Q to generate elegant piped filters
    :param request: incoming request
    :return: rendered HTML template with dashboard data
    """
    statuses = (
        ('ping', 'Ping'),
        ('ssh', 'Secure Shell Socket (SSH)'),
        ('dns', 'Domain Name Server (DNS)'),
        ('smtp', 'Email Protocol (SMTP)'),
        ('ssl', 'Secure Socket Layer (SSL)')
    )
    orders = Order.objects.filter(user=request.user)
    tickets = Ticket.objects.filter(Q(status='open') | Q(status='answered'), user=request.user)
    invoices = Invoice.objects.filter(paid=False, user=request.user)
    apis = API.objects.filter(user=request.user)
    try:
        # ENTER IN MAIN NODE URL/ACCESS POINT
        r = requests.get(url='')
        r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        network = {
            'label': 'red',
            'status': 'INACTIVE'
        }
    else:
        network = {
            'label': 'green',
            'status': 'ACTIVE'
        }
    return render(request=request, template_name='interface/dashboard.html', context={
        'orders': orders,
        'orders_count': orders.filter(status='active').count(),
        'invoices_count': invoices.count(),
        'tickets_count': tickets.count(),
        'amount_due': sum(i.get_total_cost() for i in invoices) if len(invoices) > 0 else 0,
        'apis': apis[:5],
        'network': network,
        'statuses': statuses
    })


@login_required
def settings(request):
    """
    Purpose: User general settings
    :param request: incoming request
    :return: rendered HTML template with UserSettingsForm
    """
    if request.method == 'POST':
        form = UserSettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request=request, message='You have successfully updated your settings.')
        else:
            messages.error(request=request, message='Your input was invalid. Please try again.')
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request=request, template_name='interface/settings.html', context={
        'form': form
    })


def register(request):
    """
    Purpose: Register new user
    :param request: incoming register request
    :return: rendered HTML with respective response
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('interface:dashboard'))
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                return render(request=request, template_name='registration/register_done.html', context={})
        else:
            form = UserRegisterForm()
        return render(request=request, template_name='registration/register.html', context={
            'form': form
        })


def error_404(request):
    """
    Purpose: Custom 404 page
    :param request: incoming request
    :return: rendered HTML template
    """
    return render(request=request, template_name='interface/404.html', context={})


def error_500(request):
    """
    Purpose: Custom 500 page
    :param request: incoming request
    :return: rendered HTML template
    """
    return render(request=request, template_name='interface/500.html', context={})


def custom_login(request, **kwargs):
    """
    Purpose: Custom login view to check if user is authenticated
    :param request: incoming request
    :param kwargs: keyword arguments used in routes
    :return: login auth view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('interface:dashboard'))
    return login(request=request, **kwargs)


def custom_password(request, **kwargs):
    """
    Purpose: Custom password reset view to check if user is authenticated
    :param request: incoming request
    :param kwargs: keyword arguments used in routes
    :return: password reset auth view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('interface:dashboard'))
    return password_reset(
        request=request,
        from_email='noreply@puroxy.io',
        post_reset_redirect=reverse('interface:password_reset_done'),
        html_email_template_name='registration/password_reset_email.html', **kwargs
    )


def custom_password_confirm(request, **kwargs):
    """
    Purpose: Custom password confirm view to check if user is authenticated
    :param request: incoming request
    :param kwargs: keyword arguments used in routes
    :return: password confirmation reset auth view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('interface:dashboard'))
    return password_reset_confirm(
        request=request,
        post_reset_redirect=reverse('interface:password_reset_complete'),
        **kwargs
    )


def custom_password_change(request, **kwargs):
    """
    Purpose: Custom password change view to change post_change_redirect
             to work with interface routes namespace
    :param request: incoming request
    :param kwargs: keyword arguments used in routes
    :return: password change auth view
    """
    return password_change(
        request=request,
        post_change_redirect=reverse('interface:password_change_done'),
        **kwargs
    )
