from unittest import TestCase
from .bonjour import BonjourScanner

# replace with valid data before running tests
IP = "192.168.1.2"
TYPE = "_nvstream_dbd._tcp.local."

class TestBonjourScanner(TestCase):

    def test_scan(self):
        sc = BonjourScanner()
        self.assertTrue(any(ip == IP and type == TYPE for (ip, _, type) in sc.scan()))
