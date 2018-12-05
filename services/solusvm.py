"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
import requests


class SolusVM:
    """
    Purpose: SolusVM integration class to do basic CRUD operations
    """
    def __init__(self, url, key, hash):
        """
        Purpose: Initialize SolusVM object
        :param url: base URL
        :param key: api_key found in Service Object
        :param hash: api_hash found in Service Object
        """
        self.url = url
        self.key = key
        self.hash = hash
        self.values = ({
            'rdtype': 'json',
            'hash': self.hash,
            'key': self.key
        })

    def json(self, data):
        """
        Purpose:
        :param data: data to work convert
        :return: result
        """
        result = []
        data = data.replace('><', '>...<')
        data = data.split('>')
        for i in data:
            i = i.replace('<', '')
            i = i.replace('...', '')
            i = i.split('/')[0]
            result.append(i)
        if len(result) % 2 == 0:
            result.pop()
        result = {
            result[i]: result[i + 1] for i in range(0, len(result) - 1, 2)
        }
        return result

    def query(self, action, extra=''):
        """
        Purpose:
        :param action: type of request action to make
        :param extra: extra details added to param
        :return: response
        """
        if not extra:
            self.values.update({
                'rdtype': 'json',
                'hash': self.hash,
                'key': self.key,
                'action': action
            })
            response = requests.get(
                url='https://{}/api/client/command.php'.format(self.url),
                params=self.values,
                timeout=50
            )
        else:
            response = requests.get(
                url='https://{}/api/client/command.php?key={}&hash={}&action=info&{}'.format(
                    self.url, self.key, self.hash, extra
                )
            )
        return response.text

    def reboot(self):
        """
        Purpose: Reboot VM
        :return: JSON response
        """
        return self.json(data=self.query(action='reboot'))

    def shutdown(self):
        """
        Purpose: Shutdown VM
        :return: JSON response
        """
        return self.json(data=self.query(action='shutdown'))

    def boot(self):
        """
        Purpose: Boot VM
        :return: JSON response
        """
        return self.json(data=self.query(action='boot'))

    def get_status(self):
        """
        Purpose: Retrieve status of VM
        :return: JSON response
        """
        return self.json(data=self.query(action='status'))

    def get_info(self):
        """
        Purpose: Retrieve information of VM
        :return: JSON response
        """
        return self.json(data=self.query(action='info'))

    def get_full_info(self):
        """
        Purpose: Retrieve information + extra detailed information
        :return: JSON response
        """
        extra = 'ipaddr=true&hdd=true&mem=true&bw=true'
        return self.json(data=self.query(action='info', extra=extra))
