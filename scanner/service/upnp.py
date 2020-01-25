"""
This implements a way to scan a network for all provided UPnP services.

Source:
https://williamboles.me/discovering-whats-out-there-with-ssdp/
"""

import upnpclient
from socket import gethostbyname
from urllib.parse import urlparse

class UPnPScanner:
    def scan(self):
        for device in upnpclient.discover():
            url = urlparse(device.location)
            ip = gethostbyname(url.hostname)
            for service in device.services:
                yield (ip, service.service_type)
