"""
See documentation for `run_configurations` function...
"""

from argparse import Namespace
from time import sleep
from typing import NoReturn
from pexpect.popen_spawn import PopenSpawn

from .site_config import SiteConfiguration


def run_configurations(
    args: Namespace,
    new_site: SiteConfiguration,
    shell: PopenSpawn,
) -> NoReturn:
    """Using a `SiteConfiguration` object which holds all the config commands for each access point for a site, this function establishes a serial connection that can be reused for each access point. It automatically loops through each config, waiting for prompts from the access point's console before executing the configuration commands and printin out the environment variables for confirmation on each access point. Includes minor error handling.


    Args:
    - args (`Namespace`): Arguments (from command-line or manual input)
    - new_site (`SiteConfiguration`): Object holding all config commands for the site APs being configured
    - shell (`PopenSpawn`): Shell process connecting to access point console using PuTTY Link (`plink`)
    """
    try:
        found = False
        for config in reversed(new_site.configs) if args.reverse else new_site:
            if (id := config.identifier) == args.start:
                print(f"Starting from AP {id}")
                found = True
            elif not found:
                continue

            shell.expect(".*\n*Hit <[Ee][Nn][Tt][Ee][Rr]>.*\n*")
            shell.sendline("\n\n")

            for command in config.commands:
                shell.expect("apboot>.*")
                shell.sendline(command)
                sleep(0.1)
            shell.sendline(
                "printenv group name ipaddr gatewayip dnsip domainname netmask"
            )
            print(f"Access Point {config.identifier} configured.")
            print("\n\n")
        sleep(1)
        if found:
            print("Completed configurations. Exiting program...")
        else:
            print(
                f"Starting access point not found. Valid access points: {new_site.get_range_string()}"
            )
        exit()
    except Exception:
        sleep(1)
        print("\n\nError ocurred. Exiting program...\n\n")
    except KeyboardInterrupt:
        print("\n\nProgram interrupted from keyboard. Exiting...")
