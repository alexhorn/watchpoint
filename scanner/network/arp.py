"""
This provides a way to determine all devices that are connected
to the network by sending ARP requests to all IP addresses.
"""

import struct
import socket
import time
import errno
from ..protocols.arp import ARPPacket, HARDWARE_ETHERNET, OPCODE_REQUEST, OPCODE_REPLY
from ..protocols.ethernet import EthernetPacket, ETHERTYPE_IPv4, ETHERTYPE_ARP, unpack_mac
from ..abstract_packet_scanner import AbstractPacketScanner

TIMEOUT = 30
SLEEP = 1/16

ETH_P_ALL = 0x0003
ETH_P_ARP = 0x0806

MAC_NULL = b"\x00\x00\x00\x00\x00\x00"
MAC_BROADCAST = b"\xff\xff\xff\xff\xff\xff"

class ARPScanner(AbstractPacketScanner):
    def __init__(self, interface, ip, network):
        super().__init__(TIMEOUT, SLEEP)

        self.interface = interface
        self.ip = ip
        self.network = network

    def scan(self):
        with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ARP)) as sock:
            sock.bind((self.interface, 0))
            sock.setblocking(0)

            (_, _, _, _, self.mac_addr) = sock.getsockname()

            return super().scan(list(self.network.hosts()), sock)

    def send_packet(self, target, sock):
        packet = self.__create_arp(self.mac_addr, socket.inet_aton(str(self.ip)), socket.inet_aton(str(target)))
        sock.send(packet)

    def receive_packets(self, sock):
        try:
            while True:
                data = sock.recv(4096)

                packet_eth = EthernetPacket.unpack(data)
                if packet_eth.type != ETHERTYPE_ARP:
                    continue
                
                packet_arp = ARPPacket.unpack(packet_eth.data[:28])
                if packet_arp.opcode != OPCODE_REPLY:
                    continue

                discovered_mac = unpack_mac(packet_arp.source_hw_addr)
                discovered_ip = socket.inet_ntoa(packet_arp.source_proto_addr)

                yield (discovered_ip, discovered_mac)

        except socket.error as e:
            if e.errno != errno.EAGAIN:
                # don't crash the loop on malformed packets
                print(e)

    def __create_arp(self, mac_sender, ip_sender, ip_target):
        arp_packet = ARPPacket(
            hw_addr_space = HARDWARE_ETHERNET,
            proto_addr_space = ETHERTYPE_IPv4,
            hw_addr_len = 6,
            proto_addr_len = 4,
            opcode = OPCODE_REQUEST,
            source_hw_addr = mac_sender,
            source_proto_addr = ip_sender,
            target_hw_addr = MAC_NULL,
            target_proto_addr = ip_target,
        )
        eth_packet = EthernetPacket(
            dst_addr = MAC_BROADCAST,
            src_addr = mac_sender,
            type = ETHERTYPE_ARP,
            data = arp_packet.pack()
        )
        return eth_packet.pack()
