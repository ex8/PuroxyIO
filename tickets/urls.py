"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from tickets import views


# Ticket Routes
urlpatterns = [
    url(regex=r'^$', view=views.ticket_list, name='list'),
    url(regex=r'^new/$', view=views.ticket_new, name='new'),
    url(regex=r'^(?P<uuid>[-\w]+)/$', view=views.ticket_detail, name='detail'),
    url(regex=r'^(?P<uuid>[-\w]+)/reply/$', view=views.ticket_reply, name='reply'),
]
