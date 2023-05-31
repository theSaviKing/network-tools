from blessed import Terminal
import argparse

from network.__utils__ import get_config_filename
from .devices import filter_devices
from .runconfig import run_configurations
from .site_config import SiteConfiguration

term = Terminal()


def get_usb_port():
    while (port := input("Enter name of port with USB connection to APs:\t\t")) not in (
        devs := filter_devices()
    ):
        print(
            term.orangered(
                "Error: Port does not exist or is not currently active. Check USB."
            ),
            term.orange(f"Available ports: {list(devs.keys())}"),
        )
    return port


def input_arguments():
    result = argparse.Namespace()

    global configurations
    configurations = SiteConfiguration(get_config_filename())

    result.usb_port = get_usb_port()
    while (
        start := int(input("Enter starting point for configuring next APs:\t\t"))
    ) not in configurations.get_config_list():
        print(term.orangered(f"Error: AP {start} not in config file."))
    result.start = start
    while (
        reverse := input(
            "Would you like to reverse the order of configs? [y/N]:  "
        ).lower()
    ) not in ["yes", "y", "no", "n", ""]:
        print(term.orangered("Error: Choices are Y or N"))
    result.reverse = reverse in ["yes", "y"]
    return result


def main():
    print("Importing modules and functions...", flush=True)

    print(term.move_up, term.clear_eol, end="", sep="")

    args = input_arguments()

    print(f"Access points to be configured: {configurations.get_range_string()}")

    ################################################################################
    # Consecutively configure APs by looping through config

    from pexpect.popen_spawn import PopenSpawn as ps
    from sys import stdout
    from time import sleep

    shell = ps(
        f"plink -serial {args.usb_port}", timeout=None, logfile=stdout, encoding="utf-8"
    )

    sleep(1)
    print("Ready to configure APs...\n\n")

    run_configurations(args, configurations, shell)
