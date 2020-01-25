"""
This implements a subset of the User Datagram Protocol.

Specification:
https://tools.ietf.org/html/rfc768
"""

import bitstruct
from .checksum import ip_checksum
from .ip import PROTOCOL_TCP

UDP_HEADER_STRUCT = ">u16u16u16u16"
UDP_HEADER_NAMES = ["src_port", "dst_port", "length", "checksum"]

class UDPPacket:
    def __init__(self, src_port, dst_port, length, checksum, data):
        self.src_port = src_port
        self.dst_port = dst_port
        self.length = length
        self.checksum = checksum
        self.data = data

    def pack(self):
        #return bitstruct.pack_dict(UDP_HEADER_STRUCT, UDP_HEADER_NAMES, self.__dict__) + self.data
        raise NotImplementedError()
    
    @classmethod
    def unpack(cls, packet):
        params = bitstruct.unpack_dict(UDP_HEADER_STRUCT, UDP_HEADER_NAMES, packet[:8])
        return cls(**params, data=packet[8:params["length"]])
