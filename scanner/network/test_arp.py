from unittest import TestCase
from .arp import ARPScanner
from common.config import conf_ip, conf_network, conf_interface

# replace with valid data before running tests
GATEWAY = ("192.168.1.1", "01:02:03:04:05:06")

class TestARPScanner(TestCase):

    def test_scan(self):
        sc = ARPScanner(conf_interface, conf_ip, conf_network)
        self.assertIn(GATEWAY, set(sc.scan()))
