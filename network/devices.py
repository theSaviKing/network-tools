"""Contains a few functions to get information on USB connections to device

Functions:
- `get_result`: returns result of `mode` command that list currently connected devices
- `filter_devices`: returns dictionary of currently connected devices
- `watch`: watches for changes in connected devices
"""

import subprocess, re
from typing import NoReturn
from deepdiff import DeepDiff as DD
from datetime import datetime
from blessed import Terminal
from .__utils__ import clear_screen

term = Terminal()


def get_result():
    """Runs `mode` command in Powershell to get information on currently connected USB devices

    Returns:
        res (str): List of connected USB devices and their properties
    """
    return (
        subprocess.run(["mode"], stdout=subprocess.PIPE, shell=True)
        .stdout.decode("utf-8")
        .strip()
    )


def filter_devices():
    """Parses through `mode` command output (using `get_result`) and outputs dict of USB devices and their information

    Returns:
        output (dict): USB devices and their corresponding properties
    """
    mode_input = get_result().splitlines()
    output = {}
    for line in range(len(mode_input)):
        if match := re.search("Status for device (.*):", mode_input[line]):
            device = match[1].lower()
            output[device] = {}
            continue
        if len(mode_input[line]) >= 2:
            match2 = re.search("(.*):(.*)", mode_input[line])
            if not match2:
                continue
            key = match2[1].strip().lower()
            val = match2[2].strip().lower()
            output[device][key] = val
    return output


def watch(limit: int = 0) -> NoReturn:
    """Continuously monitors USB devices connected to device, using "mode" command, and outputs observed changes. If limit != 0, runs "mode" command that amount of times instead of indefinitely.

    Args:
        limit (int, optional): Number of times to check output of "mode" command for changes. Defaults to 0.
    """
    clear_screen()
    print("Watching for USB devices")
    new_devs = filter_devices()
    print("\nCurrent devices: ", end=" ")
    print([str(x).upper() for x in new_devs.keys()])

    def check_diff():
        nonlocal new_devs
        old_devs = new_devs
        new_devs = filter_devices()
        diff = DD(old_devs, new_devs)
        if diff.get("dictionary_item_added"):
            res = str(diff.get("dictionary_item_added"))
            m = re.search("'(.*)'", res)
            dev = m[1].upper()
            change = f"Device added: {dev}"
            return datetime.now(), change
        elif diff.get("dictionary_item_removed"):
            res = str(diff.get("dictionary_item_removed"))
            m = re.search("'(.*)'", res)
            dev = m[1].upper()
            change = f"Device removed: {dev}"
            return datetime.now(), change
        return

    def output():
        last_change = check_diff()
        if last_change:
            with term.location(0, 3):
                print(term.clear_eos)
                print(
                    "*** LAST CHANGE ***",
                    last_change[1],
                    f"at {last_change[0].strftime('%a %d %B %Y, %I:%M:%S')}",
                    sep="\n",
                )

    if limit:
        for i in range(limit):
            output()
    else:
        while True:
            output()


if __name__ == "__main__":
    watch()
