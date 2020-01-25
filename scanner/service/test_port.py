from unittest import TestCase
from .port import PortScanner
from common.config import conf_ip

# replace with valid data before running tests
TARGET_IP = "192.168.1.1"
TARGET_PORTS = [*range(1, 1024)]
EXPECTED_PORTS = [21, 53, 80, 139, 445]

class TestPortScanner(TestCase):

    def test_scan(self):
        sc = PortScanner(conf_ip)
        self.assertSequenceEqual(set(sc.scan(TARGET_IP, TARGET_PORTS)), set(EXPECTED_PORTS))
