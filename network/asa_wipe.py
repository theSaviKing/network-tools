"""
Script for wiping old Cisco ASA Firewalls before being recycled.
"""


# from .devices import filter_devices
from pexpect.popen_spawn import PopenSpawn
import json

from network.__utils__ import get_usb_port

creds_file = "../creds.json"

CREDS = json.load(open(creds_file))


def main():
    usb_port = get_usb_port()
    print(f"{usb_port = }")


"""
ASA commands:

[[ Login with admin creds ]]
Username: phsadmin
Password: (see creds below)

[[ Enable terminal ]]
> enable
Password: (same password)

[[ Enter config terminal and factory reset ]]
# conf t
(config)# config factory-default
...multiple lines
(config)# exit

[[ Shutdown/uninstall SFR module ]]
# sw-module module sfr shutdown
# sw-module module sfr uninstall
"""
