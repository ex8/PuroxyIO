"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render
from payments.models import PaymentGateway
from products.models import Product


def home(request):
    """
    Purpose: Main homepage of site
    :param request: incoming request
    :return: rendered HTML template to index and with gateways
    """
    gateways = PaymentGateway.objects.all()[:4]
    return render(request=request, template_name='main/index.html', context={
        'gateways': gateways,
    })


def about(request):
    """
    Purpose: Main homepage of site
    :param request: incoming request
    :return: rendered HTML template to about
    """
    return render(request=request, template_name='main/about.html', context={})


def hosting(request):
    """
    Purpose: Web (shared) hosting page, retrieve products from DB
    :param request: incoming request
    :return: rendered HTML template to hosting
    """
    products = Product.objects.filter(type='web', available=True).order_by('price')
    return render(request=request, template_name='main/hosting.html', context={
        'products': [(products[i], products[i + 1]) for i in range(0, len(products), 2)]
    })


def xen_vps(request):
    """
    Purpose: Linux (XEN) VPS page, retrieve products from DB
    :param request: incoming request
    :return: rendered HTML template to linux-vps
    """
    products = Product.objects.filter(type='linux_vps', available=True).order_by('price')
    return render(request=request, template_name='main/linux-vps.html', context={
        'products': [(products[i], products[i + 1]) for i in range(0, len(products), 2)]
    })


def win_vps(request):
    """
    Purpose: Windows VPS page, retrieve products from DB
    :param request: incoming request
    :return: rendered HTML template to windows-vps
    """
    products = Product.objects.filter(type='window_vps', available=True).order_by('price')
    return render(request=request, template_name='main/windows-vps.html', context={
        'products': [(products[i], products[i + 1]) for i in range(0, len(products), 2)]
    })


def onshore_dedi(request):
    """
    Purpose: Onshore dedicated servers page, retrieve products from DB
    :param request: incoming request
    :return: rendered HTML template to onshore-dedicated
    """
    products = Product.objects.filter(type='onshore_dedicated', available=True).order_by('price')
    return render(request=request, template_name='main/onshore-dedicated.html', context={
        'products': [(products[i], products[i + 1]) for i in range(0, len(products), 2)]
    })


def offshore_dedi(request):
    """
    Purpose: Offshore dedicated servers page, retrieve products from DB
    :param request: incoming request
    :return: rendered HTML template to offshore-dedicated
    """
    products = Product.objects.filter(type='offshore_dedicated', available=True).order_by('price')
    return render(request=request, template_name='main/offshore-dedicated.html', context={
        'products': [(products[i], products[i + 1]) for i in range(0, len(products), 2)]
    })


def terms_of_service(request):
    """
    Purpose: Terms of service page
    :param request: incoming request
    :return: rendered HTML template to terms
    """
    return render(request=request, template_name='main/terms.html', context={})


def privacy_policy(request):
    """
    Purpose: Privacy policy page
    :param request: incoming request
    :return: rendered HTML template to privacy policy
    """
    return render(request=request, template_name='main/privacy.html', context={})


def dmca_policy(request):
    """
    Purpose: DMCA policy page
    :param request: incoming request
    :return: rendered HTML template to dmca policy
    """
    return render(request=request, template_name='main/dmca.html', context={})
