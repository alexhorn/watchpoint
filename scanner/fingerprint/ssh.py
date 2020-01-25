"""
This provides a way to determine the operating system version
of a machine that runs a SSH server.
"""

import socket

TIMEOUT=5

#https://wiki.python.org/moin/TcpCommunication 

class SSHFingerprinter:
    def fingerprint(self, ip_addr, port = 22):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip_addr, port))
            sock.settimeout(TIMEOUT)

            data = b""
            while b"\n" not in data:
                data = data + sock.recv(4096)

            (banner, _, _) = data.decode("utf-8").partition("\n")
            (_, os_ver) = banner.split(" ")

            return os_ver.strip()
