"""
Misc. methods
"""

import subprocess
from shlex import quote
from fcntl import flock, LOCK_EX
from sys import platform
from ipaddress import IPv4Address, IPv4Network

# https://unix.stackexchange.com/questions/14961/how-to-find-out-which-interface-am-i-using-for-connecting-to-the-internet
# https://unix.stackexchange.com/questions/383521/find-all-ethernet-interface-and-associate-ip-address

DEFAULT_IPV4_IFACE_CMD = "ip -4 -o route list | grep \"^default\" | awk '{print $5;}'"
IPV4_ADDR_CMD = "ip -4 -o address show dev \"{}\" | awk '{{print $4}}'"
IPV4_GATEWAY_CMD = "ip -4 -o route list dev \"{}\" | grep \"^default\" | awk '{{print $3;}}'"
SHELL_ENCODING="utf8"

def __assert_linux():
    if platform != "linux":
        raise NotImplementedError("Automatic network interface / address detection is not supported on {}".format(platform))

def __get_full_ipv4_address(iface):
    __assert_linux()
    return subprocess.check_output(IPV4_ADDR_CMD.format(quote(iface)), shell=True, encoding=SHELL_ENCODING).strip()

def get_default_ipv4_iface():
    __assert_linux()
    return subprocess.check_output(DEFAULT_IPV4_IFACE_CMD, shell=True, encoding=SHELL_ENCODING).strip()

def get_ipv4_address(iface):
    (ip, _) = __get_full_ipv4_address(iface).split("/")
    return IPv4Address(ip)

def get_ipv4_network(iface):
    return IPv4Network(__get_full_ipv4_address(iface), strict=False)

def get_ipv4_gateway(iface):
    __assert_linux()
    gateway = subprocess.check_output(IPV4_GATEWAY_CMD.format(quote(iface)), shell=True, encoding=SHELL_ENCODING).strip()
    return IPv4Address(gateway)

# https://stackoverflow.com/questions/28470246/python-lockf-and-flock-behaviour
def acquire_file_lock(path):
    file = open(path, 'w')
    flock(file, LOCK_EX)
    return file
