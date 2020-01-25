from unittest import TestCase
from binascii import unhexlify
from socket import inet_aton
from .arp import ARPPacket, HARDWARE_ETHERNET, OPCODE_REQUEST, OPCODE_REPLY
from .ethernet import EthernetPacket, ETHERTYPE_IPv4, ETHERTYPE_ARP, unpack_mac

EXAMPLE_PACKET = unhexlify("0001080006040001010203040506c0a8010c000000000000c0a80164")
EXAMPLE_TARGET_IP = inet_aton("192.168.1.100")

class TestARPPacket(TestCase):

    def test_pack_unpack(self):
        orig_packet = ARPPacket(
            hw_addr_space = HARDWARE_ETHERNET,
            proto_addr_space = ETHERTYPE_IPv4,
            hw_addr_len = 6,
            proto_addr_len = 4,
            opcode = OPCODE_REQUEST,
            source_hw_addr = b"\x01\x02\x03\x04\x05\x06",
            source_proto_addr = b"\x10\x01\x02\x03",
            target_hw_addr = b"\x02\x03\x04\x05\x06\x07",
            target_proto_addr = b"\x10\x02\x03\x04"
        )
        orig_bytes = orig_packet.pack()
        new_packet = ARPPacket.unpack(orig_bytes)
        self.assertDictEqual(orig_packet.__dict__, new_packet.__dict__)

    def test_target_ip(self):
        packet = ARPPacket.unpack(EXAMPLE_PACKET)
        self.assertEqual(packet.target_proto_addr, EXAMPLE_TARGET_IP)
