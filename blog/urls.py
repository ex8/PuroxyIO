"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from . import views

# Blog Routes
urlpatterns = [
    url(regex=r'^$', view=views.blog_list, name='list'),
    url(regex=r'^(?P<slug>[-\w]+)/$', view=views.blog_detail, name='detail')
]
