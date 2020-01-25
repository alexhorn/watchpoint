#!/usr/bin/env python3

import time
import socket
from argparse import ArgumentParser
from common.persistence import session
from common.models import Device, Heartbeat, Service, Fingerprint, Vulnerability
from sqlalchemy.orm.exc import NoResultFound
from .network.arp import ARPScanner
from .network.tr064 import TR064Scanner
from .service.port import PortScanner
from .service.upnp import UPnPScanner
from .service.bonjour import BonjourScanner
from .fingerprint.dhcp import FingerbankDHCPFingerprinter
from .fingerprint.smb import SMBFingerprinter
from .fingerprint.ssh import SSHFingerprinter
from .fingerprint.meta import MetaFingerprinter
from .vulnerability.telnet_cred import TelnetCredentialChecker
from .vulnerability.smb_cred import SMBCredentialChecker
from .data.ports import COMMON_PORTS
from common.config import conf_interface, conf_ip, conf_network, conf_arp_scan, conf_tr064_scan, conf_port_scan, \
    conf_upnp_scan, conf_bonjour_scan, conf_meta_fingerprint, conf_smb_fingerprint, conf_ssh_fingerprint, \
        conf_telnet_credential, conf_smb_credential, conf_sleep

def get_hostname(ip):
    '''Resolves an IP to a hostname (and falls back to the IP if resolving fails)'''

    try:
        (hostname, _, _) = socket.gethostbyaddr(ip)
    except socket.herror:
        return ip
    return hostname

def create_or_update_device(mac_addr, ip_addr = None, hostname = None, save_heartbeat = True):
    device = session.query(Device).filter(Device.mac_address == mac_addr).first()

    if not device:
        device = Device(
            mac_address = mac_addr
        )
        session.add(device)
    
    if ip_addr:
        device.ip_address = ip_addr

    if hostname:
        device.hostname = hostname
    elif ip_addr:
        device.hostname = get_hostname(ip_addr)

    session.commit()

    if save_heartbeat:
        heartbeat = Heartbeat(
            device_id = device.id
        )
        session.add(heartbeat)
        session.commit()

    return device

# Main part

def arp_scan():
    print("Starting ARP scan")

    arp_scanner = ARPScanner(conf_interface, conf_ip, conf_network)
    for (ip, mac) in arp_scanner.scan():
        print("Found {} at {}".format(ip, mac))

        create_or_update_device(mac_addr = mac, ip_addr = ip)

def tr064_scan():
    print("Starting TR-064 Scan")

    tr064_scanner = TR064Scanner()
    for (ip, mac, hostname) in tr064_scanner.scan():
        print("Found {} ({}) at {}".format(ip, hostname, mac))

        create_or_update_device(mac_addr = mac, ip_addr = ip, hostname = hostname, save_heartbeat = False)


def port_scan():
    port_scanner = PortScanner(str(conf_ip))

    for device in session.query(Device).filter(Device.ip_address.isnot(None)).all():
        print("Starting port scan for {}".format(device.ip_address))

        for port in port_scanner.scan(device.ip_address, COMMON_PORTS):
            print("Found {} at {}".format(port, device.ip_address))

            service = Service(
                device_id = device.id,
                type = "port",
                address = "{}/tcp".format(port),
                description = "Open port at {}/tcp".format(port)
            )
            session.add(service)
            session.commit()

def upnp_scan():
    print("Starting UPnP scan")

    upnp_scanner = UPnPScanner()
    for (ip, usn) in upnp_scanner.scan():
        try:
            device = session.query(Device).filter(Device.ip_address == ip).one()
        except NoResultFound:
            print("UPnP service {} is running on {}, but this device does not exist".format(usn, ip))
            continue

        print("Found {} at {}".format(usn, device.ip_address))

        service = Service(
            device_id = device.id,
            type = "upnp",
            address = usn,
            description = "UPnP service at {}".format(usn)
        )
        session.add(service)
        session.commit()

def bonjour_scan():
    print("Starting Bonjour scan")

    bonjour_scanner = BonjourScanner()
    for (ip, port, type) in bonjour_scanner.scan():
        try:
            device = session.query(Device).filter(Device.ip_address == ip).one()
        except NoResultFound:
            print("Bonjour service {} is running on {}, but this device does not exist".format(type, ip))
            continue
        
        print("Found {} at {}".format(type, device.ip_address))

        service = Service(
            device_id = device.id,
            type = "bonjour",
            address = type,
            description = "Bonjour service at {}".format(port)
        )
        session.add(service)
        session.commit()

def meta_fingerprint():
    print("Starting meta fingerprint")

    devices = session.query(Device).all()

    meta_fingerprinter = MetaFingerprinter()

    for device in devices:
        try:
            fp = meta_fingerprinter.fingerprint(device)
        except Exception as e:
            print(e)
            continue

        if not fp:
            continue

        for (type, value) in fp.items():
            print("Found {} at {}".format(type, device.ip_address))

            fp = Fingerprint(
                device_id = device.id,
                type = type,
                value = value
            )
            session.add(fp)
            session.commit()


def smb_fingerprint():
    print("Starting SMB fingerprint")

    device_ids = session.query(Fingerprint.device_id) \
        .filter(Fingerprint.type == "operating_system", Fingerprint.value.ilike("%windows%")) \
        .distinct()
    devices = session.query(Device) \
        .filter(Device.id.in_(device_ids), Device.ip_address.isnot(None))

    smb_fingerprinter = SMBFingerprinter()

    for device in devices.all():
        print("Found Windows device at {}".format(device.ip_address))

        try:
            (major, minor, build, _) = smb_fingerprinter.fingerprint(device.ip_address)
        except Exception as e:
            print(e)
            continue

        if not major:
            continue
            
        print("Detected version {}.{}.{} at {}".format(major, minor, build, device.ip_address))

        fp = Fingerprint(
            device_id = device.id,
            type = "operating_system_version",
            value = "{}.{}.{}".format(major, minor, build)
        )
        session.add(fp)
        session.commit()

def ssh_fingerprint():
    print("Starting SSH fingerprint")

    device_ids = session.query(Service.device_id) \
        .filter(Service.address == "22/tcp") \
        .distinct()
    devices = session.query(Device) \
        .filter(Device.id.in_(device_ids), Device.ip_address.isnot(None))

    ssh_fingerprinter = SSHFingerprinter()

    for device in devices.all():
        print("Found SSH service at {}".format(device.ip_address))

        try:
            os_ver = ssh_fingerprinter.fingerprint(device.ip_address)
        except Exception as e:
            print(e)
            continue

        if not os_ver:
            continue
            
        print("Detected version {} at {}".format(os_ver, device.ip_address))

        fp = Fingerprint(
            device_id = device.id,
            type = "operating_system_version",
            value = os_ver
        )
        session.add(fp)
        session.commit()

def telnet_credential():
    print("Starting Telnet credential check")
    
    device_ids = session.query(Service.device_id) \
        .filter(Service.address == "23/tcp") \
        .distinct()
    devices = session.query(Device) \
        .filter(Device.id.in_(device_ids), Device.ip_address.isnot(None))

    telnet_cred_checker = TelnetCredentialChecker()

    for device in devices.all():
        print("Found Telnet service at {}".format(device.ip_address))

        try:
            creds = telnet_cred_checker.check(device.ip_address)
        except Exception as e:
            print(e)
            continue

        if creds:
            print("Detected unauthenticated Telnet server at {}".format(device.ip_address))

            (username, password) = creds

            vn = Vulnerability(
                device_id = device.id,
                type = "telnet_credential",
                description = "{}:{}".format(username, password) if username and password else "(none)"
            )
            session.add(vn)
            session.commit()

def smb_credential():
    print("Starting SMB credential check")
    
    device_ids = session.query(Service.device_id) \
        .filter(Service.address == "445/tcp") \
        .distinct()
    devices = session.query(Device) \
        .filter(Device.id.in_(device_ids), Device.ip_address.isnot(None))

    smb_cred_checker = SMBCredentialChecker()

    for device in devices.all():
        print("Found SMB service at {}".format(device.ip_address))

        try:
            creds = smb_cred_checker.check(device.ip_address)
        except Exception as e:
            print(e)
            continue

        if creds:
            print("Detected unauthenticated SMB server at {}".format(device.ip_address))

            (username, password) = creds

            vn = Vulnerability(
                device_id = device.id,
                type = "smb_credential",
                description = "{}:{}".format(username, password) if username and password else "(none)"
            )
            session.add(vn)
            session.commit()

if __name__ == '__main__':
    while True:
        print("Initiating scans")

        if conf_arp_scan:
            try:
                arp_scan()
            except Exception as e:
                print(e)

        if conf_tr064_scan:
            try:
                tr064_scan()
            except Exception as e:
                print(e)

        if conf_port_scan:
            try:
                port_scan()
            except Exception as e:
                print(e)

        if conf_upnp_scan:
            try:
                upnp_scan()
            except Exception as e:
                print(e)
        
        if conf_bonjour_scan:
            try:
                bonjour_scan()
            except Exception as e:
                print(e)

        if conf_meta_fingerprint:
            try:
                meta_fingerprint()
            except Exception as e:
                print(e)

        if conf_smb_fingerprint:
            try:
                smb_fingerprint()
            except Exception as e:
                print(e)

        if conf_ssh_fingerprint:
            try:
                ssh_fingerprint()
            except Exception as e:
                print(e)
        
        if conf_telnet_credential:
            try:
                telnet_credential()
            except Exception as e:
                print(e)
        
        if conf_smb_credential:
            try:
                smb_credential()
            except Exception as e:
                print(e)

        print("Going to sleep")
        time.sleep(conf_sleep)
