import os
from blessed import Terminal
from functools import cache
from network.site_config import SiteConfiguration

term = Terminal()

clear_screen = lambda: print(term.clear, term.home, end="", flush=True)


@cache
def is_valid_config_file(filename: str):
    try:
        SiteConfiguration(filename)
    except Exception:
        return False
    else:
        return True


def find_valid_config_files():
    while not os.path.exists(
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
                    f"Error: File {file} is not valid config file. Check file contents."
                ),
                term.orange("Possibly rename file with shorter filename?")
                if len(file) > 10
                else "",
            )
    print(term.clear_eos)
    return file
