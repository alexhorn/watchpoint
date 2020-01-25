"""
This provides a way to retrieve all devices that were connected to a
network at some point from a TR-064 capable gateway.
"""

import upnpclient

USN_HOSTS1 = "urn:dslforum-org:service:Hosts:1"

PARAM_HOST_NUMBER_OF_ENTRIES = "NewHostNumberOfEntries"
PARAM_ACTIVE = "NewActive"
PARAM_IP_ADDRESS = "NewIPAddress"
PARAM_MAC_ADDRESS = "NewMACAddress"
PARAM_HOST_NAME = "NewHostName"

class TR064Scanner:
    def __init__(self):
        self.devices = None

    def __discover(self):
        '''Searches all UPnP capable devices on the network'''
        
        self.devices = upnpclient.discover()
    
    def scan(self):
        if not self.devices:
            self.__discover()
        
        for device in self.devices:
            print("Found UPnP-capable device")

            for service in device.services:
                if service.service_type != USN_HOSTS1:
                    continue

                print("Found TR-064 Hosts-capable device")

                resp_num_entries = service.GetHostNumberOfEntries()
                for i in range(0, resp_num_entries[PARAM_HOST_NUMBER_OF_ENTRIES]):
                    resp_host = service.GetGenericHostEntry(NewIndex=i)

                    # o2 HomeBox 6741 returns some entries with None or 0.0.0.0 as the IP address
                    if resp_host[PARAM_ACTIVE] and resp_host[PARAM_IP_ADDRESS] not in (None, "0.0.0.0"):
                        yield (resp_host[PARAM_IP_ADDRESS], resp_host[PARAM_MAC_ADDRESS], resp_host[PARAM_HOST_NAME])
