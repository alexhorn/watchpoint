from unittest import TestCase
from .upnp import UPnPScanner
from common.config import conf_ip, conf_network, conf_interface

# replace with valid data before running tests
GATEWAY = ("192.168.1.1", "urn:schemas-upnp-org:service:WANIPConnection:1")

class TestARPScanner(TestCase):

    def test_scan(self):
        sc = UPnPScanner()
        self.assertTrue(GATEWAY in sc.scan())
