"""
This provides a way to determine the operating system version
of a machine that runs Windows and has SMB (network file sharing) enabled.
"""

import uuid
import struct
from smbprotocol.connection import Connection, Dialects, SMB2HeaderResponse, NtStatus
from smbprotocol.session import Session, SMB2SessionSetupResponse
from smbprotocol.exceptions import SMBAuthenticationError
from ntlm_auth.messages import ChallengeMessage

NTLMSSP_MAGIC_NUMBER = b"NTLMSSP\x00\x02\x00\x00\x00"
NTLM_VERSION_STRUCT = "<BBHxxxB"

TIMEOUT = 5

class SMBFingerprinter:
    def __init__(self):
        pass

    def fingerprint(self, ip_addr, port=445):
        try:
            # connect and attempt authentication
            connection = Connection(uuid.uuid4(), ip_addr, port, require_signing=False)
            connection.connect(Dialects.SMB_2_0_2, timeout=TIMEOUT)
            try:
                session = Session(connection, "", "", require_encryption=False) # dont require encryption or signing to support o2 HomeBox

                try:
                    session.connect()
                except SMBAuthenticationError:
                    # ignore authentication error
                    # the result doesn't matter as long as there was an attempt
                    pass
                
                for packet in session.preauth_integrity_hash_value:

                    # find a STATUS_MORE_PROCESSING_REQUIRED response
                    if not isinstance(packet, SMB2HeaderResponse) or not packet["status"].value == NtStatus.STATUS_MORE_PROCESSING_REQUIRED:
                        continue
                    
                    sess_resp_bytes = packet["data"].value

                    # parse session setup response
                    sess_resp = SMB2SessionSetupResponse()
                    sess_resp.unpack(sess_resp_bytes)

                    chlg_mesg_bytes = sess_resp["buffer"].value
                    
                    # skip if this is not a NTLMSSP challenge
                    # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/801a4681-8809-4be9-ab0d-61dcfe762786
                    if not chlg_mesg_bytes.startswith(NTLMSSP_MAGIC_NUMBER):
                        continue

                    # parse NTLMSSP challenge
                    # (labelled "security blob" in wireshark)
                    chlg_mesg = ChallengeMessage(chlg_mesg_bytes)

                    # parse the version field
                    # https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/b1a6ceb2-f8ad-462b-b5af-f18527c48175
                    return struct.unpack(NTLM_VERSION_STRUCT, chlg_mesg.version.to_bytes(8, byteorder='little'))
                
                return (None, None, None, None)
            finally:
                connection.disconnect()
        except Exception as e:
            print("SMB connection failed")
            print(e)
            return (None, None, None, None)