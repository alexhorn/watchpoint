"""
This implements a way to scan a network for all provided
Bonjour (DNS-SD via mDNS) services.
"""

from time import sleep
from socket import inet_ntop, AF_INET, AF_INET6
from zeroconf import Zeroconf, ServiceBrowser, IPVersion

TIMEOUT = 5
IPV4_LENGTH = 4
IPV6_LENGTH = 16
# from https://stackoverflow.com/questions/18884422/discover-ios-device-name-using-mdns/27506247#27506247
META_SERVICE = "_services._dns-sd._udp.local."

class _TypeListener:
    def __init__(self):
        self.types = []

    def add_service(self, zeroconf, type, name):
        self.types.append(name)

    def remove_service(self, zeroconf, type, name):
        self.types.remove(name)

class _InfoListener:
    def __init__(self):
        self.infos = []

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        self.infos.append(info)
    
    def remove_service(self, zeroconf, type, name):
        self.infos = list(filter(lambda x: x.name != name, self.infos))

class BonjourScanner:
    def __get_zeroconf(self):
        return Zeroconf(ip_version=IPVersion.All)

    def __scan_types(self):
        zeroconf = self.__get_zeroconf()
        try:
            listener = _TypeListener()
            browser = ServiceBrowser(zeroconf, META_SERVICE, listener)
            sleep(TIMEOUT)
            return listener.types
        finally:
            zeroconf.close()

    def __scan_info(self, type):
        zeroconf = self.__get_zeroconf()
        try:
            listener = _InfoListener()
            browser = ServiceBrowser(zeroconf, type, listener)
            sleep(TIMEOUT)
            return listener.infos
        finally:
            zeroconf.close()

    def scan(self):
        for type in self.__scan_types():
            print("Searching for services of type {} ...".format(type))

            for service in self.__scan_info(type):
                port = service.port

                for address in service.addresses:
                    if len(address) == IPV4_LENGTH:
                        ip = inet_ntop(AF_INET, address)
                    elif len(address) == IPV6_LENGTH:
                        ip = inet_ntop(AF_INET6, address)
                    else:
                        raise ValueError("Bonjour service address has {} bytes, what is this?".format(len(address)))

                    yield (ip, port, type)
