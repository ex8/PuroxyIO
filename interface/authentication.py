"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Purpose: Email Authentication Middleware added in settings.py
    """
    def authenticate(self, username=None, password=None):
        """
        Purpose: Authenticate user using username as key
        :param username: string
        :param password: string
        :return:
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(raw_password=password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, id):
        """
        Purpose: Retrieve user from ID
        :param id: string
        :return: User
        """
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
