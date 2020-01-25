from unittest import TestCase
from binascii import unhexlify
from socket import inet_aton
from .ethernet import EthernetPacket, ETHERTYPE_IPv4, ETHERTYPE_ARP, unpack_mac

class TestEthernetPacket(TestCase):

    def test_pack_unpack(self):
        orig_packet = EthernetPacket(
            dst_addr = b"\x01\x02\x03\x04\x05\x06",
            src_addr = b"\x02\x03\x04\x05\x06\x07",
            type = ETHERTYPE_IPv4,
            data = b"Hello, World"
        )
        orig_bytes = orig_packet.pack()
        new_packet = EthernetPacket.unpack(orig_bytes)
        self.assertDictEqual(orig_packet.__dict__, new_packet.__dict__)
