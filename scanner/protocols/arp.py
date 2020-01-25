"""
This implements a subset of the ARP protocol.

Specification:
https://tools.ietf.org/html/rfc826
"""

import bitstruct

ARP_STRUCT = ">u16u16u8u8u16r48r32r48r32"
ARP_NAMES = ["hw_addr_space", "proto_addr_space", "hw_addr_len", "proto_addr_len", "opcode", "source_hw_addr", "source_proto_addr", "target_hw_addr", "target_proto_addr"]

HARDWARE_ETHERNET = 1
OPCODE_REQUEST = 1
OPCODE_REPLY = 2

class ARPPacket:
    def __init__(self, hw_addr_space, proto_addr_space, hw_addr_len, proto_addr_len, opcode, source_hw_addr, source_proto_addr, target_hw_addr, target_proto_addr):
        self.hw_addr_space = hw_addr_space
        self.proto_addr_space = proto_addr_space
        self.hw_addr_len = hw_addr_len
        self.proto_addr_len = proto_addr_len
        self.opcode = opcode
        self.source_hw_addr = source_hw_addr
        self.source_proto_addr = source_proto_addr
        self.target_hw_addr = target_hw_addr
        self.target_proto_addr = target_proto_addr

    @classmethod
    def unpack(cls, packet):
        params = bitstruct.unpack_dict(ARP_STRUCT, ARP_NAMES, packet)
        return cls(**params)

    def pack(self):
        return bitstruct.pack_dict(ARP_STRUCT, ARP_NAMES, self.__dict__)
