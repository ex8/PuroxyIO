"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.conf.urls import url
from interface import views
from django.contrib.auth.views import logout, logout_then_login, password_change_done, \
    password_reset_complete, password_reset_done
from interface.forms import AuthForm, ExtendedPasswordResetForm, ExtendedSetPasswordForm

# Interface Routes
urlpatterns = [
    url(regex=r'^$', view=views.dashboard, name='dashboard'),
    # url(regex=r'^dummy/$', view=views.dummy, name='dummy'),
    url(regex=r'^settings/$', view=views.settings, name='settings'),
    url(regex=r'^register/$', view=views.register, name='register'),
    url(regex=r'^login/$', view=views.custom_login, name='login', kwargs={
        'authentication_form': AuthForm
    }),
    url(regex=r'^logout/$', view=logout, name='logout'),
    url(regex=r'^logout-then-login/$', view=logout_then_login, name='logout_then_login'),
    url(regex=r'^password-reset/$', view=views.custom_password, name='password_reset', kwargs={
        'password_reset_form': ExtendedPasswordResetForm
    }),
    url(regex=r'^password-reset/done/$', view=password_reset_done, name='password_reset_done'),
    url(regex=r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        view=views.custom_password_confirm, name='password_reset_confirm',
        kwargs={'set_password_form': ExtendedSetPasswordForm}),
    url(regex=r'^password-reset/complete/$', view=password_reset_complete,
        name='password_reset_complete'),
    url(regex=r'^password-change/$', view=views.custom_password_change, name='password_change'),
    url(regex=r'^password-change/done/$', view=password_change_done, name='password_change_done'),
]
