import json
from datetime import datetime

import requests


def to_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.strptime(value, format).replace(tzinfo=None)
    except ValueError:
        return datetime.now().replace(tzinfo=None)


class LaunchLibraryClient:
    """
    Client for API LaunchLibrary
    Docs: https://launchlibrary.net/docs/1.4/api.html
    """

    host = 'https://launchlibrary.net/1.4/'
    result_names = {
        'agency': 'agencies',
        'agencytype': 'types',
        'rocket': 'rockets',
        'launch': 'launches',
    }

    def request(self, url):
        response = requests.get(url)
        print(url)
        if not response or response.status_code != 200:
            return {}
        return json.loads(response.content)

    def get_list(self, method, **kwargs):
        result = []
        offset = count = 0
        method_url = '{}{}?offset='.format(self.host, method)

        while True:
            data = self.request('{}{}'.format(method_url, offset))
            if not data:
                print('Broken data', method_url, offset, data)
                break
            result.extend(data.get(self.result_names.get(method)))
            total = data.get('total')
            count += data.get('count')
            offset += 30
            if count >= total:
                break

        return result

    def get_items(self, method, **kwargs):
        method_url = '{}{}'.format(self.host, method)
        params = '&'.join(['{}={}'.format(key, value) for key, value in kwargs.items()])
        if params:
            method_url = '{}?{}'.format(method_url, params)

        data = self.request(method_url)
        if data.get('count'):
            return data.get(self.result_names.get(method))

        return False

    def get_item(self, method, id):
        method_url = '{}{}/{}'.format(self.host, method, id)

        data = self.request(method_url)
        if data.get('count'):
            return data.get(self.result_names.get(method))[0]

        return False
