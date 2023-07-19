"""Main entry point for Network Tools"""

try:
    import consolemenu
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
]


prompt_args = lambda: consolemenu.SelectionMenu.get_selection(
    choices,
    "Welcome to the Network Tools utility!\n\n\nUse any of these tools to assist in configuring network equipment. To exit any of the tools during execution, use Ctrl+C.",
    "Please select an option from the list:",
)


def config_file_check():
    from network.__utils__ import get_config_filename
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


def experiment():
    from network.__utils__ import get_config_filename, clear_screen
    from network.site_config import SiteConfiguration
    import code

    def console_exit():
        raise SystemExit

    config = SiteConfiguration(get_config_filename("Enter name of config file:"))
    clear_screen()
    banner = f"""This interactive Python terminal will allow you to experiment with a SiteConfiguration object.\n\nThe object has been generated from the file you chose:\n\t{config.filepath}\nand you can access the methods/functions and attributes for that object using the 'config' variable.\n\nFor help on how to interact with object, use help(config).\n\nTo exit the interactive terminal, use exit()."""
    exitmsg = """"""
    shell = code.InteractiveConsole(
        {**globals(), **locals(), "config": config, "exit": console_exit}
    )
    shell.interact(banner=banner, exitmsg=exitmsg)


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
