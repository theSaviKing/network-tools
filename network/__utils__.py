"""
A series of useful functions for the network-tools package
"""
import os
from blessed.win_terminal import Terminal
from functools import cache
from network.site_config import SiteConfiguration

term = Terminal()

clear_screen = lambda: print(term.clear, term.home, end="", flush=True)


@cache
def is_valid_config_file(filename: str):
    """
    Checks if the specified file is a valid configuration file.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a valid configuration file, False otherwise.
    """
    try:
        SiteConfiguration(filename)
    except Exception:
        return False
    else:
        return True


def find_valid_config_files():
    """
    Finds and displays the valid configuration files in a specified directory.
    """
    while not os.path.isdir(
        directory := input(
            term.clear_eos
            + term.salmon(
                "\n* ./  -- current directory\n* ../ -- up one level\n\nName of directory to check for config files:  "
            )
        )
    ):
        print(term.orangered("Path does not exist."))
    valid_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                if is_valid_config_file(file_path):
                    valid_files.append(file_path)
    valid = "\n".join(valid_files)
    clear_screen()
    print(
        term.salmon1(
            "\n"
            + (
                f"Available config files:\n{valid}"
                if valid
                else f"No available configs in '{directory}' directory"
            )
        ),
        term.move_xy(0, 0),
        end="",
    )


def get_config_filename(
    prompt: str = "Enter filename containing all configs for the APs (leave blank to search for valid config files):",
):
    """
    Prompts the user to enter the filename of the configuration file or searches for valid config files.

    Args:
        prompt (str, optional): The prompt to display. Defaults to "Enter filename containing all configs for the APs (leave blank to search for valid config files):".

    Returns:
        str: The name of the configuration file.
    """
    while (
        not_file := not os.path.isfile((file := input(prompt.strip() + "\t")))
    ) or not is_valid_config_file(file):
        if file == "":
            find_valid_config_files()
        elif not_file:
            print(term.orangered(f"Error: File {file} does not exist."))
        else:
            print(
                term.orangered(
                    f"Error: File {file} is not a valid config file. Check file contents."
                ),
                term.orange("Possibly rename file with a shorter filename?")
                if len(file) > 10
                else "",
            )
    print(term.clear_eos)
    return file


from network.devices import filter_devices


def get_usb_port():
    """
    Prompt the user to enter the name of the port with the desired USB connection and validate its existence.

    Returns:
        str: The name of the USB port.
    """
    while (port := input("Enter name of port with USB connection to APs:\t\t")) not in (
        devs := filter_devices()
    ):
        lines = 2
        print(term.clear_eos, end="")
        if port != "":
            print(
                term.orangered(
                    "Error: Port does not exist or is not currently active. Check USB."
                )
            )
            lines += 1
        print(
            term.orange(f"Available ports: {list(devs.keys())}"),
        )
        if valid := [dev for dev in devs.keys() if dev not in ["com3", "con"]]:
            print(term.coral(f"Suggested port: {valid[0]}"))
            lines += 1
        print(term.move_up(lines), term.clear_eol, end="", sep="")
    print(term.clear_eos, end="")
    return port


def config_file_check():
    from network.site_config import SiteConfiguration

    cont = True
    while cont:
        config = SiteConfiguration(get_config_filename("Enter name of config file:"))
        rng, gaps = config.get_range_string(True, True)
        print(f"\nIncluded configs:\t{rng}\nGaps in configs:\t{gaps or 'None'}")
        with term.cbreak():
            print("\n\nCheck another file? [y/N]:  ", end="", flush=True)
            cont = (key := str(term.inkey()).lower()) not in [
                "n",
                "no",
                "\r",
                "\n",
                "",
                " ",
            ]
        clear_screen()
