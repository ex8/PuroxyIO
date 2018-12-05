"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from payments import views

# Payment Routes
urlpatterns = [
    url(regex=r'^ipn/$', view=views.ipn, name='ipn'),
    url(regex=r'^(?P<uuid>[-\w]+)/$', view=views.gateway_list, name='list'),
    url(regex=r'^(?P<uuid>[-\w]+)/(?P<slug>[-\w]+)/$', view=views.process, name='process'),
    url(regex=r'^(?P<uuid>[-\w]+)/(?P<slug>[-\w]+)/success/$', view=views.success, name='success'),
    url(regex=r'^(?P<uuid>[-\w]+)/(?P<slug>[-\w]+)/cancelled/$', view=views.cancelled, name='cancelled'),
]
