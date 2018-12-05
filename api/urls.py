"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from api import views


# API Routes
urlpatterns = [
    url(regex=r'^$', view=views.api_list, name='list'),
    url(regex=r'^services/$', view=views.service_list, name='service_list'),
    url(regex=r'^invoices/$', view=views.invoice_list, name='invoice_list'),
    url(regex=r'^tickets/$', view=views.ticket_list, name='ticket_list'),
    url(regex=r'^(?P<uuid>[-\w]+)/$', view=views.api_detail, name='detail'),
]
