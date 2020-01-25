"""
This file contains the ports that are scanned on every device

Sources:
https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
https://gist.github.com/pwnsdx/cc82feb97f451f26c24b
"""

# System ports (without port 0) plus iTunes WiFi Sync port
COMMON_PORTS = [*range(1,1023), 62078]
