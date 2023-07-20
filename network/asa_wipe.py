"""
Script for wiping old Cisco ASA Firewalls before being recycled. Must have a Python file called `creds.py` with a variable called `creds` that holds all credentials for each ASA firewall to be wiped. Format: `list[dict["code": str, "pass": str]]`

Example::
```
    # creds.py
    creds = [
        {"code": "RNDFWL001", "pass": "1234567890"},
        {"code": "ABCFWL001", "pass": "abcdefghij"},
    ]
```
"""


from signal import SIGABRT
from sys import stdout
from time import sleep
from pexpect.popen_spawn import PopenSpawn as ps
from blessed import Terminal

from network.__utils__ import get_usb_port
from .creds import creds

term = Terminal()


def get_cred():
    while (
        code := input("Enter the site code of the ASA to be wiped:\t\t").upper()
    ) not in (codes := [cred["code"][:3] for cred in creds]):
        print(
            term.orangered(
                "Invalid sitecode. Please enter a valid three-letter sitecode."
            )
        )
        print(term.move_y(2) + term.clear_eol, end="")
    print(term.clear_eos, end="")
    return creds[codes.index(code)]


def main():
    """
    Main entry point for wiping Cisco ASAs
    """
    usb_port = get_usb_port()
    cred = get_cred()
    print("\nConnecting to ASA...\n\n")
    try:
        shell = ps(
            f"plink -serial {usb_port}", timeout=None, logfile=stdout, encoding="utf-8"
        )
    except Exception as e:
        print(f"Connection failed: {e}")
    try:
        run_shell_commands(shell, cred)
    except Exception as e:
        print(f"Oops... Something didn't work: {e}")


def run_shell_commands(shell: ps, cred):
    shell.expect("Use SPACE")
    sleep(0.1)
    shell.sendline(" ")
    shell.expect("Username")
    sleep(0.1)
    shell.sendline("phsadmin")
    shell.expect("Password")
    sleep(0.15)
    shell.sendline(cred["pass"])
    valid = shell.expect(["#", "Username"])
    if valid != 0:
        raise ValueError("Password was incorrect, for some reason. Check creds.")
    sleep(0.1)
    shell.sendline("conf t")
    shell.expect("(config)#")
    sleep(0.1)
    shell.sendline("config factory-default")
    shell.expect("(config)#")
    sleep(0.1)
    shell.sendline("exit")
    shell.expect("ciscoasa#")
    sleep(0.1)
    shell.sendline("sw-module module sfr shutdown")
    sleep(0.1)
    shell.sendline("")
    while (response := shell.expect(["Shutdown issued", "cannot be shut down"])) != 0:
        shell.sendline("sw-module module sfr shutdown")
        sleep(0.1)
        shell.sendline("")
    shell.sendline("sw-module module sfr uninstall")
    sleep(0.1)
    shell.sendline("")
    while (
        response := shell.expect(
            ["Uninstall issued", "Module sfr cannot be uninstalled"]
        )
    ) != 0:
        shell.sendline("sw-module module sfr uninstall")
        sleep(0.1)
        shell.sendline("")
    shell.expect("#")
    shell.sendline("erase flash: ")
    sleep(0.1)
    shell.sendline("")
    sleep(0.1)
    shell.sendline("")
    sleep(30)
    shell.kill(SIGABRT)


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
