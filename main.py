"""Main entry point for Network Tools"""

from network.__utils__ import config_file_check
from network.site_config import experiment


try:
    import consolemenu
    import cutie
    from contextlib import suppress
    from blessed.win_terminal import Terminal
    from network.__utils__ import clear_screen
except ModuleNotFoundError as e:
    print(
        f"\nYou do not have some of the required modules to run this program. Please install them using this command:  pip install -r requirements.txt\n\nException:{e}"
    )
    exit()

term = Terminal()

choices = [
    "Provision access points",
    "Check for gaps in config file",
    "Experiment with SiteConfiguration object from file",
    "Generate AP SN/MAC spreadsheet template",
    "Merge fragmented spreadsheets",
    "Wipe a Cisco ASA Firewall",
    term.gray30("Requires valid firewall credentials to automatically log in"),
]


# prompt_args = lambda: consolemenu.SelectionMenu.get_selection(
#     choices,
#     "Welcome to the Network Tools utility!\n\n\nUse any of these tools to assist in configuring network equipment. To exit any of the tools during execution, use Ctrl+C.",
#     "Please select an option from the list:",
# )


def prompt_args() -> int:
    clear_screen()
    print(
        term.bold_crimson("\nWelcome to the Network Tools utility!"),
        "\tUse any of these tools to assist in working with network equipment.",
        term.coral("\tTo exit any of the tools during execution, ")
        + term.bold_coral("use Ctrl+C."),
        sep="\n",
        end="\n\n",
    )
    print(
        term.yellow("Please select an option from the list:"),
        "(use ↑/↓ + ENTER to select)",
        end="\n\n",
    )
    ch = cutie.select(choices, [6], caption_prefix="    * ")
    clear_screen()
    return ch


if __name__ == "__main__":
    while True:
        with suppress(BaseException):
            match (choice := prompt_args()):
                case 0:
                    from network import provision

                    provision.main()
                case 1:
                    config_file_check()
                case 2:
                    experiment()
                case 3 | 4:
                    from network.spreadsheet import (
                        generate_spreadsheet_template,
                        merge_spreadsheets,
                    )

                    if choice == 3:
                        generate_spreadsheet_template()
                    else:
                        merge_spreadsheets()
                case 5:
                    from network import asa_wipe

                    asa_wipe.main()
                case _:
                    break
        with suppress(ValueError):
            print(
                term.clear_eos
                + "\n\nContinue? ('q' to quit program, anything else to return):  ",
                end="",
            )
            with term.cbreak():
                if term.inkey() == "q":
                    clear_screen()
                    break
