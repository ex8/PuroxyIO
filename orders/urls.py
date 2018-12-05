"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from orders import views

# Order Routes
urlpatterns = [
    url(regex=r'^$', view=views.order_list, name='list'),
    url(regex=r'^(?P<slug>[-\w]+)/$', view=views.order_detail, name='detail'),
]
