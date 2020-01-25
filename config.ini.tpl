[behavior]
sleep = 300
debug = False

[persistence]
database = /var/lib/watchpoint/db.sqlite

[network]

[strategies]
arp_scan = yes
tr064_scan = yes
port_scan = yes
upnp_scan = yes
bonjour_scan = yes
dhcp_fingerprint = yes
dhcp_fingerprint_via_fingerbank = yes
meta_fingerprint = yes
smb_fingerprint = yes
ssh_fingerprint = yes
telnet_credential = yes
smb_credential = yes

[credentials]
fingerbank_api_key =
