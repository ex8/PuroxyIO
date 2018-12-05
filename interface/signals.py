"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""

from django.contrib.auth.signals import user_logged_in
from interface.email import SendEmail
from django.dispatch import receiver
from interface.models import Email


@receiver(signal=user_logged_in)
def login_notify_email(sender, request, user, **kwargs):
    """
    Purpose: Send login notification email, received signal from Django
             auth signals; user logged in
    :param sender: sender of signal
    :param request: request associated with signal
    :param user: user at hand for signal
    :param kwargs: keyword arguments
    :return: N/A
    """
    if user.is_superuser is False:
        SendEmail(
            subject='Notification of connection to interface',
            to_email=user.email,
            data={
                'first_name': user.first_name
            },
            template='login-notify',
            user=user
        ).send()
        Email.objects.create(
            subject='Notification of Connection to PuroxyIO Interface',
            to_email=user.email,
            from_email='noreply@puroxy.io',
            from_name='PuroxyIO',
            body='Login notification',
            user=user
        )
