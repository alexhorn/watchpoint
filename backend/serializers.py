"""
This contains methods that convert raw SQLAlchemy objects
into dictionaries that can be safely sent to the user as JSON
"""

from time import time
from scanner.data.vendors import Vendors

vendors = Vendors()

def serialize_device(device):
    return {
        "id": device.id,
        "mac_address": device.mac_address,
        "ip_address": device.ip_address,
        "hostname": device.hostname,
        "label": device.label
    }

def serialize_device_details(device, services, fingerprints, vulnerabilities, last_heartbeat, activity_hours, activity_weekdays):
    return {
        "id": device.id,
        "label": device.label,
        "hostname": device.hostname,
        "ip_address": device.ip_address,
        "mac_address": device.mac_address,
        "mac_vendor": vendors.lookup(device.mac_address),
        "services": list(map(serialize_service, services)),
        "fingerprints": list(map(serialize_fingerprint, fingerprints)),
        "vulnerabilities": list(map(serialize_vulnerability, vulnerabilities)),
        "last_heartbeat": last_heartbeat.timestamp if last_heartbeat else None,
        "activity": {
            "hours": activity_hours,
            "weekdays": activity_weekdays
        }
    }

def serialize_service(service):
    return {
        "id": service.id,
        "timestamp": service.timestamp,
        "type": service.type,
        "address": service.address,
        "description": service.description
    }

def serialize_fingerprint(fingerprint):
    return {
        "id": fingerprint.id,
        "timestamp": fingerprint.timestamp,
        "type": fingerprint.type,
        "value": fingerprint.value
    }

def serialize_vulnerability(vulnerability):
    return {
        "id": vulnerability.id,
        "timestamp": vulnerability.timestamp,
        "type": vulnerability.type,
        "description": vulnerability.description
    }
