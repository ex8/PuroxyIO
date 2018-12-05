"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class UserRegisterForm(forms.ModelForm):
    """
    Purpose: Create user registration form
             Initialize two (2) password fields for confirmation before creating
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'large-input-ticket',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'large-input-ticket',
        'placeholder': 'Password again'
    }))
    captcha = ReCaptchaField(widget=ReCaptchaWidget(size='compact'))

    class Meta:
        """
        Purpose: Meta class used for ModelForm.
                 Edit input attributes for respective CSS class
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'large-input-ticket',
                'placeholder': 'Username',
                'autofocus': 'autofocus'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'large-input-ticket',
                'placeholder': 'First name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'large-input-ticket',
                'placeholder': 'Last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'large-input-ticket',
                'placeholder': 'Email',
                'required': True
            })
        }

    def clean_password2(self):
        """
        Purpose: Validate (clean) if password one (1) and password two (2) are the same
        :return: password two (2)
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_username(self):
        """
        Purpose: Validate (clean) if username exists within DB (must be unique)
        :return: username
        """
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        """
        Purpose: Validate (clean) if email exists within DB (must be unique)
        :return: email
        """
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already exists')
        return email


class UserSettingsForm(forms.ModelForm):
    """
    Purpose: User settings form
    """
    class Meta:
        """
        Purpose: Meta class used for ModelForm
                Edit input attributes for respective CSS class
        """
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'large-input-settings',
                'placeholder': 'First name',
                'autofocus': 'autofocus',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'large-input-settings',
                'placeholder': 'Last name',
                'required': True
            })
        }

    def clean(self):
        """
        Purpose: Validate (clean) entire form if potentially an extended Profile exists
        :return: N/A
        """
        pass


class AuthForm(AuthenticationForm):
    """
    Purpose: Authentication form used for Login auth view, passed in routes
             Inherit from AuthenticationForm to override
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email or username',
        'autofocus': 'autofocus'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))


class ExtendedPasswordResetForm(PasswordResetForm):
    """
    Purpose: Password reset form extended for Password Reset auth view, passed in routes
             Inherit from PasswordResetForm to override
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'autofocus': 'autofocus'
    }))


class ExtendedSetPasswordForm(SetPasswordForm):
    """
    Purpose: Set New Password Form for SetPassword auth view, passed in routes
             Inherit from SetPasswordForm to override
    """
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New password',
        'autofocus': 'autofocus'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New password again'
    }))
