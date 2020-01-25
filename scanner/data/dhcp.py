"""
This file contains DHCP fingerprints that can be used to determine the
operating system of a device.

Source:
https://gfiber.googlesource.com/vendor/google/platform/+/master/taxonomy/dhcp.py
Licensed under the Apache License
"""

DATABASE = {
    '1,33,3,6,15,26,28,51,58,59': ['android'],
    '1,33,3,6,15,28,51,58,59': ['android'],
    '1,3,6,28,33,51,58,59,121': ['android'],
    '1,121,33,3,6,15,28,51,58,59,119': ['android'],
    '1,3,6,15,26,28,51,58,59,43': ['android'],
    '1,3,6,15,112,113,78,79,95,252': ['appletv1'],
    '6,3,1,15,66,67,13,44,2,42,12': ['brotherprinter'],
    '1,3,6,15,44,47': ['canonprinter'],
    '1,121,33,3,6,12,15,26,28,51,54,58,59,119,252': ['chromeos'],
    '1,121,33,3,6,12,15,26,28,51,54,58,59,119': ['chromeos'],
    '1,3,6': ['dashbutton', 'canonprinter'],
    '1,3,6,28': ['ecobee', 'canonprinter'],
    '1,3,6,12,15,17,28,40,41,42': ['epsonprinter'],
    '6,3,1,15,66,67,13,44': ['hpprinter'],
    '6,3,1,15,66,67,13,44,12': ['hpprinter'],
    '6,3,1,15,66,67,13,44,12,81': ['hpprinter'],
    '6,3,1,15,66,67,13,44,119,12,81,252': ['hpprinter'],
    '6,3,1,15,66,67,13,44,12,81,252': ['hpprinter'],
    '1,3,6,15,119,252': ['ios'],
    '1,121,3,6,15,119,252': ['ios'],
    '1,3,6,15,119,95,252,44,46,47': ['ipodtouch1'],
    '252,3,42,15,6,1,12': ['lgtv', 'tizen'],
    '252,3,42,6,1,12': ['tizen'],
    '1,3,6,15,119,95,252,44,46,101': ['macos'],
    '1,3,6,15,119,95,252,44,46': ['macos'],
    '1,121,3,6,15,119,252,95,44,46': ['macos'],
    '58,59,6,15,51,54,1,3': ['panasonictv'],
    '1,3,15,6': ['playstation'],
    '1,3,6,15,12': ['roku'],
    '1,3,6,12,15,28,42,125': ['samsungtv'],
    '1,28,2,3,15,6,12': ['tivo'],
    '1,3,6,12,15,28,42': ['viziotv', 'wemo', 'directv', 'samsungtv'],
    '1,3,6,12,15,28,40,41,42': ['viziotv', 'kindle'],
    '1,3,6,12,15,17,23,28,29,31,33,40,41,42': ['viziotv'],
    '1,3,6,15,28,33': ['wii'],
    '1,3,6,15': ['wii', 'xbox'],
    '1,15,3,6,44,46,47,31,33,121,249,252,43': ['windows-phone', 'windows'],
    '1,3,6,15,31,33,43,44,46,47,121,249,252': ['windows'],
}
