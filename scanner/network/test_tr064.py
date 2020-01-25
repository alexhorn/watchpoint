from unittest import TestCase
from .tr064 import TR064Scanner
from common.config import conf_ip, conf_network, conf_interface

# replace with valid data before running tests
DESKTOP = ("192.168.1.2", "01:02:03:04:05:06", "DESKTOP-ABCDEFG")

class TestARPScanner(TestCase):

    def test_scan(self):
        sc = TR064Scanner()
        self.assertTrue(DESKTOP in sc.scan())
