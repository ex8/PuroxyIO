"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.core.mail import EmailMessage
from interface.models import Email
from django.contrib.auth.models import User

FROM_EMAIL = 'noreply@puroxy.io'
FROM_NAME = 'PuroxyIO'


class SendEmail:
    """
    Purpose: Email class used site-wide integrated with sparkpost
    """
    def __init__(self, subject='', to_email='', data='', template='', user=''):
        """
        Purpose:
        :param subject: email subject string
        :param to_email: receiver's email
        :param data: dictionary contained k/v pairs to render
        :param template: sparkpost email template name
        :param user: user FK
        """
        self.subject = subject
        self.to_email = to_email
        self.data = data or {}
        self.template = template
        self.user = user

    def send(self):
        """
        Purpose: Send email to email address & create email object
        """
        m = EmailMessage(
            subject=self.subject,
            to=[{
                'address': self.to_email,
                'substitution_data': self.data
            }],
            from_email=FROM_EMAIL
        )
        m.template = self.template
        m.send()
        self.create_email_object()

    def notify_admins(self):
        """
        Purpose: Notify all super admins via e-mail
        """
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            self.data['first_name'] = admin.first_name
            m = EmailMessage(
                subject=self.subject,
                to=[{
                    'address': admin.email,
                    'substitution_data': self.data
                }],
                from_email=FROM_EMAIL
            )
            m.template = self.template
            m.send()

    def create_email_object(self):
        """
        Purpose: Used to create Email object internally,
                can be used to display on site for client
        """
        Email.objects.create(
            subject=self.subject,
            to_email=self.to_email,
            from_email=FROM_EMAIL,
            from_name=FROM_NAME,
            body=self.data,
            user=self.user
        )
