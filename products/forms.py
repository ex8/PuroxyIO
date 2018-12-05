"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django import forms
from products.models import ProductConfigurationOptionItem
import validators
from services.models import Service


class ProductConfigurationForm(forms.Form):
    """
    Purpose: Create ProductConfiguration form from ProductConfigurationOption and Items
    """
    def __init__(self, options, *args, **kwargs):
        super(ProductConfigurationForm, self).__init__(*args, **kwargs)
        for option in options:
            if option.type == 'input':
                self.fields[option.name] = forms.CharField()
                self.fields[option.name].widget.attrs.update({
                    'class': 'option-input-size',
                    'placeholder': option.name
                })
            elif option.type == 'dropdown':
                items = ProductConfigurationOptionItem.objects.filter(option=option)
                choices = [('', option.name)] + [(i, i) for i in items]
                self.fields[option.name] = forms.ChoiceField(choices=choices)
                self.fields[option.name].widget.attrs.update({
                    'class': 'select-style'
                })

    def clean(self):
        """
        Purpose: Validate (clean) if domain is a valid URL/TLD
        :return: data
        """
        data = super(ProductConfigurationForm, self).clean()
        if 'Domain (example.com)' in data:
            domain = data['Domain (example.com)']
            if not validators.domain(domain):
                raise forms.ValidationError(message='Invalid URL/TLD', code='invalid')
            if Service.objects.filter(hostname=domain).exists():
                raise forms.ValidationError(message='Domain already exists in the system', code='invalid')
        return data


class ProductAddOnForm(forms.Form):
    """
    Purpose: Create ProductAddOn Form from ProductAddOn objects passed in
    """
    def __init__(self, addons, *args, **kwargs):
        super(ProductAddOnForm, self).__init__(*args, **kwargs)
        for addon in addons:
            self.fields[addon.name] = forms.CharField(
                widget=forms.CheckboxInput,
                required=False,
                help_text='{} -- {} (${})'.format(
                    addon.name, addon.description, addon.price
                )
            )
