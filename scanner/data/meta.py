"""
This file contains signatures that are used to fingerprint devices based on
their metadata (open ports, available upnp/bonjour services, hostname, etc.)
"""

MAPPINGS = [
    {
        "ports": ["135/tcp", "139/tcp", "445/tcp"], # msrpc and smb
        "hostname": r"^DESKTOP-",
        "operating_system": "windows",
        "class": "pc"
    },
    {
        "ports": ["62078/tcp"], # itunes wifi sync
        "operating_system": "ios"
    },
    {
        "hostname": r"^iPhone",
        "class": "phone",
        "operating_system": "ios"
    },
    {
        "hostname": r"^iPad",
        "class": "tablet",
        "operating_system": "ios"
    },
    {
        "ports": ["22/tcp"], # ssh
        "operating_system": "linux"
    },
    {
        "hostname": r"^android-",
        "operating_system": "android"
    },
    {
        "ports": ["631/tcp"], # internet printing protocol
        "class": "printer"
    },
    {
        "upnp": ["urn:schemas-upnp-org:service:WANIPConnection:1"],
        "class": "router"
    }
]

MAPPING_RESULTS = ["operating_system", "class"]