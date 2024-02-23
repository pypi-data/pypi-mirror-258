import unittest
from chiarpc.harvester import HarvesterClient


class TestHarvester(unittest.TestCase):
    def test_add_plot_directory(self):
        c = HarvesterClient()
        # c.add_plot_directory('')
