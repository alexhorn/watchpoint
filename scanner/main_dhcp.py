#!/usr/bin/env python3

from sqlalchemy.orm.exc import NoResultFound
from common.persistence import session
from common.models import Device, Heartbeat, Service, Fingerprint
from .fingerprint.dhcp import OfflineDHCPFingerprinter, FingerbankDHCPFingerprinter
from .main import create_or_update_device
from common.config import conf_dhcp_fingerprint, conf_dhcp_fingerprint_via_fingerbank, conf_fingerbank_api_key

def persist_dhcp_fingerprint(mac_addr, os_match):
    print("Storing DHCP fingerprint for {}".format(mac_addr))

    device = create_or_update_device(mac_addr)

    fp = Fingerprint(
        device_id = device.id,
        type = "operating_system",
        value = os_match
    )
    session.add(fp)
    session.commit()

def dhcp_fingerprint():
    print("Starting DHCP fingerprint")

    if conf_dhcp_fingerprint_via_fingerbank:
        dhcp_fingerprinter = FingerbankDHCPFingerprinter(conf_fingerbank_api_key)
    else:
        dhcp_fingerprinter = OfflineDHCPFingerprinter()
    
    for (mac_addr, os_match) in dhcp_fingerprinter.listen():
        persist_dhcp_fingerprint(mac_addr, os_match)

if __name__ == '__main__':
    while True:
        if not conf_dhcp_fingerprint:
            print("DHCP fingerprinting disabled")
            exit(1)
        
        dhcp_fingerprint()
