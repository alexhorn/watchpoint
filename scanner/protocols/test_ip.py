from unittest import TestCase
from binascii import unhexlify
from socket import inet_aton
from .ip import IPPacket, PROTOCOL_TCP
from .checksum import ip_checksum

class TestIPPacket(TestCase):

    def test_pack_unpack(self):
        orig_packet = IPPacket(
            version = 4, # IPv4
            ihl = 5, # depends on other stuff in header
            tos = 0, # irrelevant
            len = 32, 
            id = 1234,
            flags = 0,
            frag_offset = 0,
            ttl = 50,
            proto = PROTOCOL_TCP,
            checksum = b"",
            src_addr = b"\x10\x01\x02\x03",
            dst_addr = b"\x10\x02\x03\x04",
            data = b"Hello, World"
        )
        orig_bytes = orig_packet.pack()
        new_packet = IPPacket.unpack(orig_bytes)
        self.assertDictEqual(orig_packet.__dict__, new_packet.__dict__)
        self.assertEqual(len(orig_bytes), new_packet.len)
        self.assertEqual(ip_checksum(orig_bytes[:len(orig_bytes)-len(new_packet.data)]), 0)
