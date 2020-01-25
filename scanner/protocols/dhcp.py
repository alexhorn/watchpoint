"""
This implements a subset of the Dynamic Host Configuration Protocol.

Specifications:
https://tools.ietf.org/html/rfc2131
https://tools.ietf.org/html/rfc2132
"""

import bitstruct

DHCP_STRUCT = ">u8u8u8u8u32u16u16r32r32r32r32r128r512r1024"
DHCP_NAMES = ["op", "htype", "hlen", "hops", "xid", "secs", "flags", "ciaddr", "yiaddr", "siaddr", "giaddr", "chaddr", "sname", "file"]

DHCP_CORE_HEADER_LENGTH = 44 # without sname/file
DHCP_FULL_HEADER_LENGTH = 236 # with sname/file
DHCP_OPTION_PAD = 0
DHCP_OPTION_END = 255
DHCP_OPTIONS_MAGIC_COOKIE = b"\x63\x82\x53\x63" # denotes the start of the options field

class DHCPPacket:
    def __init__(self, op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file, options):
        self.op = op
        self.htype = htype
        self.hlen = hlen
        self.hops = hops
        self.xid = xid
        self.secs = secs
        self.flags = flags
        self.ciaddr = ciaddr
        self.yiaddr = yiaddr
        self.siaddr = siaddr
        self.giaddr = giaddr
        self.chaddr = chaddr
        self.sname = sname
        self.file = file
        self.options = options

    @classmethod
    def unpack(cls, packet):
        # the options field may extend into sname/file
        # so we have to extract the options into their own variable
        # TODO: check option overload option before reading options out of sname/file
        options_idx = packet.index(DHCP_OPTIONS_MAGIC_COOKIE, DHCP_CORE_HEADER_LENGTH)
        header_bytes = packet[:options_idx].rjust(DHCP_FULL_HEADER_LENGTH, b"\x00")
        options_bytes = packet[options_idx+len(DHCP_OPTIONS_MAGIC_COOKIE):]

        params = bitstruct.unpack_dict(DHCP_STRUCT, DHCP_NAMES, header_bytes)
        options = list(DHCPOption.parse_multiple(options_bytes))

        params["chaddr"] = params["chaddr"][:params["hlen"]]
        params["sname"] = params["sname"][:params["sname"].index(b"\x00")]
        params["file"] = params["file"][:params["file"].index(b"\x00")]

        return cls(**params, options=options)
    
    def pack(self):
        raise NotImplementedError

    def get_option(self, code):
        for option in self.options:
            if option.code == code:
                return option.data
        return None

class DHCPOption:
    def __init__(self, code, data):
        self.code = code
        self.data = data
    
    @classmethod
    def parse_multiple(cls, packet):
        i = 0
        while i < len(packet):
            code = packet[i]
            i = i + 1

            if code == DHCP_OPTION_PAD:
                continue
            elif code == DHCP_OPTION_END:
                return

            length = packet[i]
            i = i + 1

            data = packet[i:i+length]
            i = i + length

            yield cls(code, data)
