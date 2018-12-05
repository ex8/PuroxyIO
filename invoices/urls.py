"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from invoices import views


# Invoices Routes
urlpatterns = [
    url(regex=r'^$', view=views.invoice_list, name='list'),
    url(regex=r'^(?P<uuid>[-\w]+)/$', view=views.invoice_detail, name='detail'),
]
