"""
This provides a way to capture DHCP fingerprints from a
network interface and determine the requesters device
or operating system.
"""

import socket
import time
import errno
from difflib import SequenceMatcher
import requests
from ..protocols.ip import IPPacket
from ..protocols.udp import UDPPacket
from ..protocols.dhcp import DHCPPacket
from ..protocols.arp import HARDWARE_ETHERNET
from ..protocols.ethernet import unpack_mac
from ..data.dhcp import DATABASE

ETHERNET_ADDR_LENGTH = 6
DHCP_PORT = 67
DHCP_BOOTREQUEST = 1
DHCP_OPTION_MESSAGE_TYPE = 53
DHCP_OPTION_PARAM_REQ_LIST = 55
DHCP_MESSAGE_TYPE_DISCOVER = 1

# https://wiki.python.org/moin/UdpCommunication

def compare_fingerprints(a, b):
    """Returns a number between 0..1 that indicates the similarity between the two fingerprints"""

    if isinstance(a, str):
        a = [int(x) for x in a.split(",")]
    if isinstance(b, str):
        b = [int(x) for x in b.split(",")]

    matcher = SequenceMatcher(None, a, b)
    total_size = 0
    for block in matcher.get_matching_blocks():
        total_size = total_size + block.size
    return total_size / max(len(a), len(b))

def get_dhcp_option(packet, name):
    return next(val for key, val in packet.options if key == name)

class BaseDHCPFingerprinter:
    def match_fingerprint(self, fingerprint):
        raise NotImplementedError()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as sock:
            sock.bind(("", 0))

            while True:
                try:
                    data, _ = sock.recvfrom(4096)

                    ip_packet = IPPacket.unpack(data)

                    udp_packet = UDPPacket.unpack(ip_packet.data)

                    if udp_packet.dst_port != DHCP_PORT:
                        continue

                    dhcp_packet = DHCPPacket.unpack(udp_packet.data)

                    if dhcp_packet.op != DHCP_BOOTREQUEST or dhcp_packet.htype != HARDWARE_ETHERNET:
                        continue

                    msg_type = dhcp_packet.get_option(DHCP_OPTION_MESSAGE_TYPE)[0]

                    if msg_type != DHCP_MESSAGE_TYPE_DISCOVER:
                        continue

                    req_list = list(dhcp_packet.get_option(DHCP_OPTION_PARAM_REQ_LIST)) # convert the binary string into a list of integers
                    
                    sender_mac = unpack_mac(dhcp_packet.chaddr[:ETHERNET_ADDR_LENGTH])
                    os_match = self.match_fingerprint(req_list)

                    yield (sender_mac, os_match)
                except Exception as e:
                    print(e)

class OfflineDHCPFingerprinter(BaseDHCPFingerprinter):
    """DHCP fingerprinter that uses an offline database for fingerprint lookups"""

    def match_fingerprint(self, fingerprint):
        (_, matches) = max(DATABASE.items(), key=lambda fp: compare_fingerprints(fingerprint, fp[0]))
        return matches[-1] # last one seems more sensible

class FingerbankDHCPFingerprinter(BaseDHCPFingerprinter):
    """DHCP fingerprinter that uses fingerbank.org to perform fingerprint lookups"""

    def __init__(self, fingerbank_api_key):
        self.fingerbank_api_key = fingerbank_api_key

    def match_fingerprint(self, fingerprint):
        payload = {
            "key": self.fingerbank_api_key,
            "dhcp_fingerprint": ",".join(str(x) for x in fingerprint)
        }

        resp = requests.get("https://api.fingerbank.org/api/v2/combinations/interrogate", params=payload)
        if resp.status_code == 404:
            return None
        
        name = resp.json()["device"]["name"]
        
        return name
