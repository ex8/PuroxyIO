"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django import forms


class ServerFunctionForm(forms.Form):
    """
    Purpose: Create form used to POST SolusVM and WHM from detail
    """
    hidden = forms.CharField(required=False, widget=forms.HiddenInput())
