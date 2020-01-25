"""
This implements a subset of the Ethernet protocol.

Source:
Computer networking: a top-down approach by Kurose, James F. and Ross, Keith W., Chapter 6.4.2
"""

import struct
import bitstruct

ETHERNET_HEADER_STRUCT = ">r48r48u16"
ETHERNET_HEADER_NAMES = ["dst_addr", "src_addr", "type"]

ETHERTYPE_IPv4 = 0x800
ETHERTYPE_ARP = 0x806

ETHERNET_HEADER_LENGTH = 14

# from https://stackoverflow.com/questions/4959741/python-print-mac-address-out-of-6-byte-string
def pack_mac(str):
    return struct.pack("BBBBBB", *(int(x, 16) for x in str.split(":")))

def unpack_mac(mac):
    return "{0:02x}:{1:02x}:{2:02x}:{3:02x}:{4:02x}:{5:02x}".format(*struct.unpack("BBBBBB", mac))

class EthernetPacket:
    def __init__(self, dst_addr, src_addr, type, data):
        self.dst_addr = dst_addr
        self.src_addr = src_addr
        self.type = type
        self.data = data

    @classmethod
    def unpack(cls, packet):
        params = bitstruct.unpack_dict(ETHERNET_HEADER_STRUCT, ETHERNET_HEADER_NAMES, packet[:ETHERNET_HEADER_LENGTH])
        return cls(**params, data=packet[ETHERNET_HEADER_LENGTH:])
    
    def pack(self):
        return bitstruct.pack_dict(ETHERNET_HEADER_STRUCT, ETHERNET_HEADER_NAMES, self.__dict__) + self.data
