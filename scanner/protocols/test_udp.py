from unittest import TestCase
from binascii import unhexlify
from .udp import UDPPacket

EXAMPLE = unhexlify("e409076c00916f8964617461")
EXAMPLE_DATA = b"data"

class TestUDPPacket(TestCase):

    def test_unpack(self):
        reference_packet = UDPPacket(
            src_port = 58377,
            dst_port = 1900,
            length = 145,
            checksum = 0x6f89,
            data = EXAMPLE_DATA
        )
        example_packet = UDPPacket.unpack(EXAMPLE)
        self.assertDictEqual(reference_packet.__dict__, example_packet.__dict__)
