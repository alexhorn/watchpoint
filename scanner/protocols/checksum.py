"""
This implements the IP checksum algorithm.

Sources:
https://tools.ietf.org/html/rfc791
http://mathforum.org/library/drmath/view/54379.html
"""

import struct

def ip_checksum(payload):
    sum = 0
    for i in range(0, len(payload), 2):
        sum = sum + struct.unpack("!H", payload[i:i+2].rjust(2, b"\x00"))[0]
        if sum > 0xFFFF:
            # move carry-out into least significant bits
            sum = (sum & 0xFFFF) + (sum >> 16)
    return 0xFFFF - sum
