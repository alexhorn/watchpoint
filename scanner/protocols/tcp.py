"""
This implements a subset of the Transmission Control Protocol.
Does not implement options.

Specification:
https://tools.ietf.org/html/rfc793
"""

import bitstruct
from .checksum import ip_checksum
from .ip import PROTOCOL_TCP

PSEUDO_IP_HEADER_STRUCT = ">r32r32p8u8u16"
PSEUDO_IP_HEADER_NAMES = ["src_addr", "dst_addr", "protocol", "tcp_len"]
TCP_HEADER_STRUCT = ">u16u16u32u32u4p6u1u1u1u1u1u1u16u16u16"
TCP_HEADER_NAMES = ["src_port", "dst_port", "seq_nr", "ack_nr", "offset", "urg", "ack", "psh", "rst", "syn", "fin", "window", "checksum", "urgent"]

TCP_HEADER_LENGTH = 20 # without options

class TCPPacket:
    def __init__(self, src_port, dst_port, seq_nr, ack_nr, offset, urg, ack, psh, rst, syn, fin, window, checksum, urgent, data, src_addr = b"", dst_addr = b""):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_nr = seq_nr
        self.ack_nr = ack_nr
        self.offset = offset
        self.urg = urg
        self.ack = ack
        self.psh = psh
        self.rst = rst
        self.syn = syn
        self.fin = fin
        self.window = window
        self.checksum = checksum
        self.urgent = urgent
        self.data = data
        self.src_addr = src_addr
        self.dst_addr = dst_addr

    def pack(self):
        self.checksum = 0
        options = 4 * b"\x00" # not including this makes Wireshark suspicious

        # construct fake packet for checksum calculation
        tcp_packet = bitstruct.pack_dict(TCP_HEADER_STRUCT, TCP_HEADER_NAMES, self.__dict__) + options
        ip_header = bitstruct.pack_dict(PSEUDO_IP_HEADER_STRUCT, PSEUDO_IP_HEADER_NAMES, {
            "src_addr": self.src_addr,
            "dst_addr": self.dst_addr,
            "protocol": PROTOCOL_TCP,
            "tcp_len": len(tcp_packet)
        })

        # construct real packet
        self.checksum = ip_checksum(ip_header + tcp_packet + self.data)
        return bitstruct.pack_dict(TCP_HEADER_STRUCT, TCP_HEADER_NAMES, self.__dict__) + options + self.data
    
    @classmethod
    def unpack(cls, packet):
        params = bitstruct.unpack_dict(TCP_HEADER_STRUCT, TCP_HEADER_NAMES, packet[:TCP_HEADER_LENGTH])
        return cls(**params, data=packet[params["offset"] * 4:])
