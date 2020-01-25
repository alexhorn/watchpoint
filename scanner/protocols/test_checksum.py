from unittest import TestCase
from binascii import unhexlify
from .checksum import ip_checksum

# "010203040506" with trailing checksum
EXAMPLE_PACKET = unhexlify("010203040506F6F3")

class TestChecksum(TestCase):

    def test_checksum(self):
        checksum = ip_checksum(EXAMPLE_PACKET)
        self.assertEqual(checksum, 0)
