"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from services import views


# Service Routes
urlpatterns = [
    url(regex=r'^$', view=views.service_list, name='list'),
    url(regex=r'^(?P<uuid>[-\w]+)/$', view=views.service_detail, name='detail'),
]
