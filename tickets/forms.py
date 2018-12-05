"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django import forms
from tickets.models import Ticket, Response
from services.models import Service


class NewTicketForm(forms.ModelForm):
    """
    Purpose: Create new ticket form
    """

    class Meta:
        """
        Purpose: Meta class data used for ModelForm
        """
        model = Ticket
        fields = ('subject', 'priority', 'service', 'message')
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'large-input-subject',
                'placeholder': 'Subject',
                'autofocus': 'autofocus'
            }),
            'priority': forms.Select(attrs={
                'class': 'select-style'
            }),
            'service': forms.Select(attrs={
                'class': 'select-style'
            }),
            'message': forms.Textarea(attrs={
                'class': 'large-input-ticket',
                'cols': 30,
                'rows': 20,
                'type': 'text',
                'placeholder': 'Please describe your issue/concern/request as descriptive as you can so we can '
                               'effectively assist you.'
            })
        }

    def __init__(self, user, *args, **kwargs):
        """
        Purpose: Initialize NewTicketForm with filtered queryset on field
        :param user: requested user
        :param args: arguments
        :param kwargs: keyword arguments
        """
        super(NewTicketForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(user=user)


class CloseTicketForm(forms.Form):
    """
    Purpose: Create close ticket form
    """
    hidden = forms.CharField(required=False, widget=forms.HiddenInput())


class ReplyForm(forms.ModelForm):
    """
    Purpose: Create ticket reply form
    """
    class Meta:
        """
        Purpose: Meta class data for ModelForm
        """
        model = Response
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'large-input-ticket',
                'type': 'text',
                'placeholder': 'Please enter a ticket response'
            })
        }
