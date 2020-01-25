"""
This provides a way to scan a device for all open ports.
"""

import socket
import time
import errno
import random
import struct
from ..protocols.tcp import TCPPacket
from ..protocols.ip import IPPacket
from ..protocols.ethernet import EthernetPacket
from ..abstract_packet_scanner import AbstractPacketScanner

def str_to_mac(str):
    return struct.pack("BBBBBB", *(int(x, 16) for x in str.split(":")))

def mac_to_str(mac):
    return "{0:02x}:{1:02x}:{2:02x}:{3:02x}:{4:02x}:{5:02x}".format(*struct.unpack("BBBBBB", mac))

TIMEOUT = 5
SLEEP = 1/256

# from https://stackoverflow.com/a/312464
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class PortScanner(AbstractPacketScanner):
    def __init__(self, src_ip):
        super().__init__(TIMEOUT, SLEEP)

        self.src_ip = src_ip
        self.src_port = random.randrange(1, 65536)

    def scan(self, dst_ip, dst_ports):
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as sock:
            sock.bind((str(self.src_ip), 0))
            sock.setblocking(0)

            return super().scan(dst_ports, sock, dst_ip)

    def send_packet(self, dst_port, sock, dst_ip):
        packet = self.__create_syn(dst_ip, dst_port)
        sock.sendto(packet, (dst_ip, dst_port))
    
    def receive_packets(self, sock, dst_ip):
        try:
            while True:
                data, (sender_addr, _) = sock.recvfrom(4096)

                ip_packet = IPPacket.unpack(data)

                tcp_packet = TCPPacket.unpack(ip_packet.data)
                
                if sender_addr == dst_ip and tcp_packet.syn == 1 and tcp_packet.ack == 1:
                    yield tcp_packet.src_port

        except socket.error as e:
            if e.errno != errno.EAGAIN:
                # don't crash the loop on malformed packets
                print(e)

    def __create_syn(self, dst_ip, dst_port):
        tcp_packet = TCPPacket(
            src_port = self.src_port,
            dst_port = dst_port,
            seq_nr = 0,
            ack_nr = 0,
            offset = 6, # header length
            urg = 0,
            ack = 0,
            psh = 0,
            rst = 0,
            syn = 1,
            fin = 0,
            window = 0,
            checksum = 0,
            urgent = 0,
            data = b"",
            src_addr = socket.inet_aton(str(self.src_ip)),
            dst_addr = socket.inet_aton(str(dst_ip)),
        )
        return tcp_packet.pack()
