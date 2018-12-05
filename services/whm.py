"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
import base64
import http.client
import urllib.parse
import json
from interface.email import SendEmail


class WHM:
    """
    Purpose: WHM/cPanel integration class to do basic CRUD operations
    """
    def __init__(self, url, username, password):
        """
        Purpose: Initialize WHM object
        :param url: Base URL
        :param username: WHM username
        :param password: WHM password
        """
        self.url = url
        self.credentials = bytes('{}:{}'.format(username, password), encoding='ascii')
        self.headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode(self.credentials).decode('ascii'))
        }

    def query(self, resource, kwargs):
        """
        Purpose: Query and send request to WHM API v1
        :param resource:
        :param kwargs:
        :return:
        """
        try:
            kwargs['api.version'] = 1
            connection = http.client.HTTPSConnection(self.url, 2087)
            connection.request(
                'GET',
                '/json-api/{}?{}'.format(resource, urllib.parse.urlencode(kwargs)),
                headers=self.headers
            )
            response = connection.getresponse()
            data = json.loads(response.read().decode('utf-8'))
            connection.close()
            return data
        except http.client.HTTPException as e:
            SendEmail(
                subject='',
                data=str(e),
                template='cpanel-error-admin'
            ).notify_admins()

    def create(self, username, password, domain, plan):
        """
        Purpose: Create new cPanel account
        :param username: cPanel username
        :param password: cPanel password
        :param domain: cPanel domain
        :param plan: WHM plan
        :return: response data
        """
        return self.query(resource='createacct', kwargs={
            'username': username,
            'password': password,
            'domain': domain,
            'plan': plan
        })

    def suspend(self, username, reason):
        """
        Purpose: Suspend cPanel account
        :param username: cPanel username
        :param reason: suspension reasoning
        :return: response data
        """
        return self.query(resource='suspendacct', kwargs={
            'user': username,
            'reason': reason
        })

    def unsuspend(self, username):
        """
        Purpose: Un-suspend cPanel account
        :param username: cPanel username
        :return: response data
        """
        return self.query(resource='unsuspendacct', kwargs={
            'user': username
        })

    def create_user_session(self, username, service):
        """
        Purpose: Create user cPanel session for one-time click login
        :param username: cPanel username
        :param service: always set to `cpaneld` (passed in)
        :return: response data
        """
        return self.query(resource='create_user_session', kwargs={
            'user': username,
            'service': service
        })
