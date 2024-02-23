# https://docs.chia.net/harvester-rpc/
from chiarpc.client import Client
import os.path


class HarvesterClient:
    def __init__(self, base_url=None, cert_file=None, key_file=None):
        if base_url is None:
            base_url = 'http://localhost:8560'
        if cert_file is None or key_file is None:
            home_path = os.path.expanduser("~")
            ssl_path = os.path.join(home_path, '.chia', 'mainnet', 'config', 'ssl')
            if cert_file is None:
                cert_file = os.path.join(ssl_path, 'harvester', 'private_harvester.crt')
            if key_file is None:
                key_file = os.path.join(ssl_path, 'harvester', 'private_harvester.key')
        self.client = Client(base_url, cert_file, key_file)

    def add_plot_directory(self, dirname: str):
        return self.client.request('add_plot_directory',
                                   data={'dirname': dirname})
