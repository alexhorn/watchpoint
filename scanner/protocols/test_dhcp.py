from unittest import TestCase
from binascii import unhexlify
from .dhcp import DHCPPacket, DHCPOption

# DHCP discover from an Amazon Kindle
EXAMPLE = unhexlify("01010600c6d0831d000000000000000000000000000000000000000001020304050600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000638253633501013d07010102030405063902024037070103060c0f1c2a3c0c756468637020312e32382e33ff0000000000000000000000000000000000000000")

class TestDHCPPacket(TestCase):

    def test_unpack(self):
        self.maxDiff = None
        reference_options = [
            DHCPOption(code = 53, data = unhexlify("01")),
            DHCPOption(code = 61, data = unhexlify("01010203040506")),
            DHCPOption(code = 57, data = unhexlify("0240")),
            DHCPOption(code = 55, data = unhexlify("0103060c0f1c2a")),
            DHCPOption(code = 60, data = unhexlify("756468637020312e32382e33"))
        ]
        reference_packet = DHCPPacket(
            op = 1,
            htype = 1,
            hlen = 6,
            hops = 0,
            xid = 0xc6d0831d,
            secs = 0,
            flags = 0,
            ciaddr = b"\x00\x00\x00\x00",
            yiaddr = b"\x00\x00\x00\x00",
            siaddr = b"\x00\x00\x00\x00",
            giaddr = b"\x00\x00\x00\x00",
            chaddr = b"\x01\x02\x03\x04\x05\x06",
            sname = b"",
            file = b"",
            options = reference_options
        )
        example_packet = DHCPPacket.unpack(EXAMPLE)

        # test options separately
        reference_dict = dict((x, y) for (x, y) in reference_packet.__dict__.items() if x != "options")
        example_dict = dict((x, y) for (x, y) in example_packet.__dict__.items() if x != "options")

        self.assertDictEqual(reference_dict, example_dict)
        self.assertSequenceEqual([x.__dict__ for x in reference_options], [x.__dict__ for x in example_packet.options])
