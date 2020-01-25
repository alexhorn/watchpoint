"""
This parses the configuration files to provide variables
that can be imported to access the applications configuration
"""

from configparser import ConfigParser
from os import path, getenv
from ipaddress import IPv4Address, IPv4Network
from .utils import get_default_ipv4_iface, get_ipv4_address, get_ipv4_network

DEFAULT_CONFIG_FILE = "./config.dev.ini"

config = ConfigParser()
config.read(getenv("WATCHPOINT_CONFIG_FILE", DEFAULT_CONFIG_FILE))

conf_sleep = config["behavior"].getint("sleep")
conf_debug = config["behavior"].getboolean("debug")

conf_database = config["persistence"]["database"]

__default_interface = get_default_ipv4_iface()
conf_interface = config["network"].get("interface", __default_interface)
__default_ip = get_ipv4_address(conf_interface)
conf_ip = IPv4Address(config["network"].get("ip_address", __default_ip))
__default_network = get_ipv4_network(conf_interface)
conf_network = IPv4Network(config["network"].get("network_address", __default_network))

conf_fingerbank_api_key = config["credentials"]["fingerbank_api_key"]

conf_arp_scan = config["strategies"].getboolean("arp_scan")
conf_tr064_scan = config["strategies"].getboolean("tr064_scan")
conf_port_scan = config["strategies"].getboolean("port_scan")
conf_upnp_scan = config["strategies"].getboolean("upnp_scan")
conf_bonjour_scan = config["strategies"].getboolean("bonjour_scan")
conf_dhcp_fingerprint = config["strategies"].getboolean("dhcp_fingerprint")
conf_meta_fingerprint = config["strategies"].getboolean("meta_fingerprint")
conf_smb_fingerprint = config["strategies"].getboolean("smb_fingerprint")
conf_ssh_fingerprint = config["strategies"].getboolean("ssh_fingerprint")
conf_telnet_credential = config["strategies"].getboolean("telnet_credential")
conf_smb_credential = config["strategies"].getboolean("smb_credential")

conf_dhcp_fingerprint_via_fingerbank = config["strategies"].getboolean("dhcp_fingerprint_via_fingerbank")
