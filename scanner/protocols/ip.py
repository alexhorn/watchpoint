
"""
This implements a subset of the Internet Protocol.
Options are not implemented.

Specifications:
https://tools.ietf.org/html/rfc790
https://tools.ietf.org/html/rfc791
"""


import bitstruct
from .checksum import ip_checksum

IP_HEADER_STRUCT = ">u4u4u8u16u16u3u13u8u8u16r32r32"
IP_HEADER_NAMES = ["version", "ihl", "tos", "len", "id", "flags", "frag_offset", "ttl", "proto", "checksum", "src_addr", "dst_addr"]

PROTOCOL_TCP = 6

IP_HEADER_LENGTH = 20 # without options

class IPPacket:
    def __init__(self, version, ihl, tos, len, id, flags, frag_offset, ttl, proto, checksum, src_addr, dst_addr, data):
        self.version = version
        self.ihl = ihl
        self.tos = tos
        self.len = len
        self.id = id
        self.flags = flags
        self.frag_offset = frag_offset
        self.ttl = ttl
        self.proto = proto
        self.checksum = checksum
        self.src_addr = src_addr
        self.dst_addr = dst_addr
        self.data = data

    def pack(self):
        self.checksum = 0
        packet = bitstruct.pack_dict(IP_HEADER_STRUCT, IP_HEADER_NAMES, self.__dict__)
        self.checksum = ip_checksum(packet)
        return bitstruct.pack_dict(IP_HEADER_STRUCT, IP_HEADER_NAMES, self.__dict__) + self.data

    @classmethod
    def unpack(cls, bytes):
        params = bitstruct.unpack_dict(IP_HEADER_STRUCT, IP_HEADER_NAMES, bytes[:IP_HEADER_LENGTH])
        return cls(**params, data=bytes[params["ihl"] * 4:])
