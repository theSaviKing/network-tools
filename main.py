"""Main entry point for Network Tools"""

import code, consolemenu, contextlib

from blessed import Terminal

from network.site_config import SiteConfiguration
from network.__utils__ import clear_screen


term = Terminal()

choices = [
    "Provision access points",
    "Check for gaps in config file",
    "Experiment with SiteConfiguration object from file",
]


prompt_args = lambda: consolemenu.SelectionMenu.get_selection(
    choices,
    "Welcome to the Network Tools utility!\n\n\nUse any of these tools to assist in configuring network equipment. To exit any of the tools during execution, use Ctrl+C.",
    "Please select an option from the list:",
)


def config_file_check():
    from network.__utils__ import get_config_filename

    cont = True
    while cont:
        config = SiteConfiguration(get_config_filename("Enter name of config file:"))
        rng, gaps = config.get_range_string(True, True)
        print(f"\nIncluded configs:\t{rng}\nGaps in configs:\t{gaps or 'None'}")
        with term.cbreak():
            print("\n\nCheck another file? [y/N]:  ", end="", flush=True)
            cont = (key := term.inkey()) not in ["n", "no", ""]
            print(key)
        clear_screen()


def experiment():
    from network.__utils__ import get_config_filename, clear_screen

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
        with contextlib.suppress(BaseException):
            match prompt_args():
                case 0:
                    from network import provision

                    provision.main()
                case 1:
                    config_file_check()
                case 2:
                    experiment()
                case _:
                    break
        with contextlib.suppress(ValueError):
            print(
                "\n\nContinue? ('q' to quit program, anything else to return):  ",
                end="",
            )
            with term.cbreak():
                if term.inkey() == "q":
                    clear_screen()
                    break
