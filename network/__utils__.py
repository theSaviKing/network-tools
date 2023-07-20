"""
A series of useful functions for the network-tools package
"""
import os
from typing import List, Optional
from blessed.win_terminal import Terminal
from functools import cache

import readchar
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


###
#   THE FOLLOWING CODE IS ADAPTED FROM THE cutie PACKAGE BY kamik423 (License: MIT) -- `pip install cutie`
###


class DefaultKeys:
    """** ADAPTED FROM [cutie](https://github.com/kamik423/cutie) by [kamik423](https://github.com/kamik423)

    List of default keybindings.

    Attributes:
        interrupt(List[str]): Keys that cause a keyboard interrupt.
        select(List[str]): Keys that trigger list element selection.
        confirm(List[str]): Keys that trigger list confirmation.
        delete(List[str]): Keys that trigger character deletion.
        down(List[str]): Keys that select the element below.
        up(List[str]): Keys that select the element above.
    """

    interrupt: List[str] = [readchar.key.CTRL_C, readchar.key.CTRL_D]
    select: List[str] = [readchar.key.SPACE]
    confirm: List[str] = [readchar.key.ENTER]
    delete: List[str] = [readchar.key.BACKSPACE]
    down: List[str] = [readchar.key.DOWN, "j"]
    up: List[str] = [readchar.key.UP, "k"]
    numbers: List[str] = [str(n) for n in range(1, 10)]


def select(
    options: List[str],
    caption_indices: Optional[List[int]] = None,
    deselected_prefix: str = "\033[1m[ ]\033[0m ",
    selected_prefix: str = "\033[1m[\033[32;1mx\033[0;1m]\033[0m ",
    caption_prefix: str = "",
    selected_index: int = 0,
    confirm_on_select: bool = True,
) -> int:
    """** ADAPTED FROM [cutie](https://github.com/kamik423/cutie) by [kamik423](https://github.com/kamik423)

    Select an option from a list.

    Args:
        options (List[str]): The options to select from.
        caption_indices (List[int], optional): Non-selectable indices.
        deselected_prefix (str, optional): Prefix for deselected option ([ ]).
        selected_prefix (str, optional): Prefix for selected option ([x]).
        caption_prefix (str, optional): Prefix for captions ().
        selected_index (int, optional): The index to be selected at first.
        confirm_on_select (bool, optional): Select keys also confirm.

    Returns:
        int: The index that has been selected.
    """
    print("\n" * (len(options) - 1))
    if caption_indices is None:
        caption_indices = []

    def get_new_index(direction):
        new_index = selected_index + direction
        while (
            new_index >= 0 and new_index < len(options) and new_index in caption_indices
        ):
            new_index += direction
        return new_index

    while True:
        print(f"\033[{len(options) + 1}A")
        for i, option in enumerate(options):
            if i not in caption_indices:
                prefix = selected_prefix if i == selected_index else deselected_prefix
                print(f"\033[K{prefix}{option}")
            else:
                print(f"\033[K{caption_prefix}{option}")
        keypress = readchar.readkey()

        if keypress in DefaultKeys.up:
            selected_index = get_new_index(-1)
        elif keypress in DefaultKeys.down:
            selected_index = get_new_index(1)
        elif keypress in DefaultKeys.confirm or (
            confirm_on_select and keypress in DefaultKeys.select
        ):
            break
        elif keypress in DefaultKeys.numbers and int(keypress) < len(options):
            selected_index = int(keypress) - 1
        elif keypress in DefaultKeys.interrupt:
            raise KeyboardInterrupt

    return selected_index
