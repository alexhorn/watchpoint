"""
This provides a lookup table to determine the manufacturer
of a device based on its MAC address.

These files are required:
http://standards-oui.ieee.org/oui/oui.csv
http://standards-oui.ieee.org/oui28/mam.csv
http://standards-oui.ieee.org/oui36/oui36.csv
"""

import csv
from os import path

class Vendors:
    def __init__(self):
        self.dict = {}
        self.read_csv("scanner/data/ieee_oui.csv")
        self.read_csv("scanner/data/ieee_mam.csv")
        self.read_csv("scanner/data/ieee_oui36.csv")
    
    def read_csv(self, filename):
        with open(filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader) # skip header
            for row in csvreader:
                self.dict[row[1]] = row[2]

    def lookup(self, mac):
        mac = mac.replace(':', '').upper()
        if mac[:9] in self.dict:
            return self.dict[mac[:9]]
        elif mac[:7] in self.dict:
            return self.dict[mac[:7]]
        elif mac[:6] in self.dict:
            return self.dict[mac[:6]]
