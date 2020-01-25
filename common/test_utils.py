from unittest import TestCase
from ipaddress import IPv4Address, IPv4Network
from .utils import get_default_ipv4_iface, get_ipv4_address, get_ipv4_network, get_ipv4_gateway

IFACE = "wlan0"
IP = IPv4Address("192.168.1.200")
NETWORK = IPv4Network("192.168.1.0/24")
GATEWAY = IPv4Address("192.168.1.1")

class TestUtils(TestCase):

    def test_default_ipv4_iface(self):
        iface = get_default_ipv4_iface()
        self.assertEqual(iface, IFACE)

    def test_ipv4_address(self):
        ip = get_ipv4_address(IFACE)
        self.assertEqual(ip, IP)

    def test_ipv4_network(self):
        network = get_ipv4_network(IFACE)
        self.assertEqual(network, NETWORK)

    def test_ipv4_gateway(self):
        gateway = get_ipv4_gateway(IFACE)
        self.assertEqual(gateway, GATEWAY)
