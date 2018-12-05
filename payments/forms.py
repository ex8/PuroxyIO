"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django import forms


class PaymentForm(forms.Form):
    """
    Purpose: Create PaymentForm used to POST to PaymentGateway
             Initialize using HiddenInput for each field
    """
    def __init__(self, initial, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for k, v in initial.items():
            self.fields[k] = forms.CharField(initial=v, widget=forms.HiddenInput)
