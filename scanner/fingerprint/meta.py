"""
This provides a way to identify a devices characteristics
based on its metadata (open ports, provided upnp services, hostname)
"""

import re
from ..data.meta import MAPPINGS, MAPPING_RESULTS

class MetaFingerprinter:
    def fingerprint(self, device):
        """Fingerprint a device based on its metadata"""

        match = max(MAPPINGS, key=lambda mapping: self.__match_score(device, mapping), default=None)
        match_score = self.__match_score(device, match)
        if match and match_score > 0:
            return {k: v for k, v in match.items() if k in MAPPING_RESULTS}
        else:
            return None

    def __get_services(self, device, type):
        return [svc.address for svc in device.services if svc.type == type]

    def __ports_match(self, device, mapping):
        if "ports" in mapping:
            svcs = self.__get_services(device, "port")
            return all(port in svcs for port in mapping["ports"])
        else:
            return False

    def __hostname_matches(self, device, mapping):
        if device.hostname and "hostname" in mapping:
            return re.match(mapping["hostname"], device.hostname)
        else:
            return False

    def __upnp_matches(self, device, mapping):
        if "upnp" in mapping:
            svcs = self.__get_services(device, "upnp")
            return all(svc in svcs for svc in mapping.get("upnp", []))
        else:
            return False

    def __match_score(self, device, mapping):
        """Calculate a score that indicates how much this device resembles the definition"""

        ports_score = 1 if self.__ports_match(device, mapping) else 0
        hostname_score = 1 if self.__hostname_matches(device, mapping) else 0
        upnp_score = 1 if self.__upnp_matches(device, mapping) else 0
        return ports_score + hostname_score + upnp_score
