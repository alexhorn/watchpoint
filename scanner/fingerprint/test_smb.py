from unittest import TestCase
from .smb import SMBFingerprinter

# replace with valid data before running tests
DESKTOP_IP = "192.168.1.2"
DESKTOP_VERSION = (10, 0, 18362, 15)

class TestSMBFingerprinter(TestCase):

    def test_fingerprint(self):
        fp = SMBFingerprinter()
        self.assertEqual(fp.fingerprint(DESKTOP_IP), DESKTOP_VERSION)
