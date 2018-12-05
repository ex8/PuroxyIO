"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from services.models import Service
from orders.models import Order
from services.solusvm import SolusVM
from django.conf import settings
from services.forms import ServerFunctionForm
from django.contrib import messages
from services.whm import WHM


@login_required
def service_list(request):
    """
    Purpose: Retrieve service objects associated to requested user
    :param request: incoming request
    :return: rendered HTML template with services
    """
    objects = Service.objects.filter(user=request.user).order_by('-created')
    paginator = Paginator(object_list=objects, per_page=10)
    page = request.GET.get('page')
    try:
        services = paginator.page(number=page)
    except PageNotAnInteger:
        services = paginator.page(number=1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)
    return render(request=request, template_name='services/list.html', context={
        'services': services
    })


@login_required
def service_detail(request, uuid):
    """
    Purpose: Retrieve detailed service associated to user with UUID
    :param request: incoming request
    :param uuid: service universally unique identifier
    :return: rendered HTML template with detailed service
    """
    service = get_object_or_404(klass=Service, uuid=uuid, user=request.user)
    order = Order.objects.get(service=service)
    operations = False
    svm_info = {}
    os_images = {
        'centos': 'images/centos.jpg',
        'debian': 'images/debian.jpg',
        'gentoo': 'images/gentoo.jpg',
        'arch': 'images/archlinux.png',
        'ubuntu': 'images/ubuntu.jpg',
        'windows': 'images/windows.jpg',
        'unknown': 'images/unknown.jpg'
    }
    if order.product.type == 'web':
        whm = WHM(
            url=settings.WEB_HOST_BASE_URL,
            username=settings.WEB_HOST_USERNAME,
            password=settings.WEB_HOST_PASSWORD
        )
        w = whm.create_user_session(username=service.username, service='cpaneld')
    else:
        w = ''
    if order.product.type == 'linux_vps' or order.product.type == 'window_vps' \
            or order.product.type == 'onshore_dedicated':
        operations = True
        if service.api_hash and service.api_key:
            svm = SolusVM(url=settings.SOLUSVM_URL, key=service.api_key, hash=service.api_hash)
            data = svm.get_full_info()
            svm_info = {
                'hdd': data['hdd'].split(','),
                'bw': data['bw'].split(',')
            }
    if request.method == 'POST':
        form = ServerFunctionForm(data=request.POST)
        if form.is_valid():
            if service.api_hash and service.api_key:
                svm = SolusVM(url=settings.SOLUSVM_URL, key=service.api_key, hash=service.api_hash)
                if 'reboot' in request.POST:
                    svm.reboot()
                    messages.success(
                        request=request,
                        message='Your device has been rebooted. Please allow up to 5 minutes to complete.'
                    )
                elif 'boot' in request.POST:
                    svm.boot()
                    messages.success(
                        request=request,
                        message='Your device has been booted. Please allow up to 5 minutes to complete.'
                    )
                elif 'shut_down' in request.POST:
                    svm.shutdown()
                    messages.success(
                        request=request,
                        message='Your device has been shut down. Please allow up to 5 minutes to complete.'
                    )
            else:
                messages.error(
                    request=request,
                    message='There was an error making your request. Please contact support.'
                )
    else:
        form = ServerFunctionForm()
    return render(request=request, template_name='services/detail.html', context={
        'service': service,
        'order': order,
        'os_image': get_os_image(os=service.os, images=os_images),
        'product': order.product,
        'svm_info': svm_info,
        'operations': operations,
        'form': form,
        'w': w
    })


def get_os_image(os, images):
    """
    Purpose: Retrieve operating system image
    :param os: name of operating system
    :param images: dictionary of k/v -> os/image pairs
    :return:
    """
    if 'CentOS' in os:
        os_image = images['centos']
    elif 'CloudLinux' in os:
        os_image = images['centos']
    elif 'Debian' in os:
        os_image = images['debian']
    elif 'Gentoo' in os:
        os_image = images['gentoo']
    elif 'Arch' in os:
        os_image = images['arch']
    elif 'Ubuntu' in os:
        os_image = images['ubuntu']
    elif 'Windows' in os:
        os_image = images['windows']
    else:
        os_image = images['unknown']
    return os_image
