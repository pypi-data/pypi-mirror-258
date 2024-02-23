from urllib.parse import urljoin

import requests


class Client:
    def __init__(self, base_url, cert_file, key_file):
        self.base_url = base_url
        self.cert_file = cert_file
        self.key_file = key_file

    def request(self, endpoint, data):
        headers = {'Content-Type': 'application/json'}
        url = urljoin(self.base_url, endpoint)
        cert = (self.cert_file, self.key_file)
        response = requests.post(url, data=data, headers=headers, cert=cert, verify=False)
        return response.json()
