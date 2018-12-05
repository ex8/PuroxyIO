"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models
from django.conf import settings
from services.models import Service
from interface.email import SendEmail
import uuid

# Ticket status types
STATUS_CHOICES = (
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('client_response', 'Client Response'),
    ('answered', 'Answered'),
    ('closed', 'Closed')
)

# Ticket priority types
PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High')
)


class Ticket(models.Model):
    """
    Purpose: Ticket Model to document support tickets
    @uuid: universally unique identifier
    @subject: ticket subject title
    @message: body message
    @status: type of status
    @priority: type of priority
    @created: creation date, set automatically
    @updated: last time ticket was saved, set automatically
    @service: service FK
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=30)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    service = models.ForeignKey(Service, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.subject

    def get_status(self):
        """
        Purpose: Retrieve ticket status label
        :return: status dict
        """
        if self.status == 'open':
            s = {
                'label': 'green',
                'status': 'OPEN'
            }
        elif self.status == 'in_progress':
            s = {
                'label': 'red',
                'status': 'IN PROGRESS'
            }
        elif self.status == 'client_response':
            s = {
                'label': 'yellow',
                'status': 'CLIENT RESPONSE'
            }
        elif self.status == 'answered':
            s = {
                'label': 'blue',
                'status': 'ANSWERED'
            }
        elif self.status == 'closed':
            s = {
                'label': 'gray',
                'status': 'CLOSED'
            }
        else:
            s = {
                'label': 'red',
                'status': 'ERROR'
            }
        return s


class Response(models.Model):
    """
    Purpose: Ticket Response Model to document user responses to tickets
    @uuid: universally unique identifier
    @message: body message
    @created: creation date, set automatically
    @ticket: ticket FK
    @user: user FK
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Response for {}'.format(self.ticket)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Purpose: Used to send client email notification about new ADMIN response
        :return: N/A
        """
        if self.user.is_staff:
            ticket_data = {
                'first_name': self.ticket.user.first_name,
                'client': '{} {}'.format(self.ticket.user.first_name, self.ticket.user.last_name),
                'ticket_id': str(self.ticket.uuid),
                'priority': self.ticket.priority,
                'subject': self.ticket.subject,
                'message': self.message
            }
            SendEmail(
                subject='New Support Ticket',
                to_email=self.ticket.user.email,
                data=ticket_data,
                template='new-ticket-response',
                user=self.ticket.user
            ).send()
        super(Response, self).save()
