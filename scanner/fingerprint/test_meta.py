from unittest import TestCase
from .meta import MetaFingerprinter
from common.models import Device, Service

# example iOS device metadata
IOS = Device(
    mac_address = "01:02:03:04:05:06",
    ip_address = "192.168.1.1",
    hostname = "foobar",
    services = [
        Service(
            type = "port",
            address = "62078/tcp"
        )
    ]
)

class TestMetaFingerprinter(TestCase):

    def test_fingerprint(self):
        fp = MetaFingerprinter()
        res = fp.fingerprint(IOS)
        self.assertEqual(res["operating_system"], "ios")
        self.assertNotIn("class", res)
