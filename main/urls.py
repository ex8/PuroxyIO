"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from . import views

# Main-site Routes
urlpatterns = [
    url(r'^$', view=views.home, name='home'),
    url(r'^about/$', view=views.about, name='about'),
    url(r'^web-hosting/$', view=views.hosting, name='hosting'),
    url(r'^linux-vps/$', view=views.xen_vps, name='linux_vps'),
    url(r'^windows-vps/$', view=views.win_vps, name='win_vps'),
    url(r'^onshore-dedicated-servers/$', view=views.onshore_dedi, name='onshore_dedi'),
    url(r'^offshore-dedicated-servers/$', view=views.offshore_dedi, name='offshore_dedi'),
    url(r'^legal/terms/$', view=views.terms_of_service, name='terms'),
    url(r'^legal/privacy/$', view=views.privacy_policy, name='privacy'),
    url(r'^legal/dmca/$', view=views.dmca_policy, name='dmca'),
]
