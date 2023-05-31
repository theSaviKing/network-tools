"""Main entry point for Network Tools"""

import code, consolemenu, contextlib

from blessed import Terminal

from network.site_config import SiteConfiguration


term = Terminal()

choices = [
    "Provision access points",
    "Check for gaps in config file",
    "Experiment with SiteConfiguration object from file",
]


prompt_args = lambda: consolemenu.SelectionMenu.get_selection(
    choices,
    "Welcome to the Network Tools utility!",
    "Please select an option from the list:",
)


def get_config_gaps():
    from network.__utils__ import get_config_filename

    config = SiteConfiguration(get_config_filename("Enter name of config file:"))
    rng, gaps = config.get_range_string(True, True)
    print(f"\nIncluded configs:\t{rng}\nGaps in configs:\t{gaps or 'None'}")


def experiment():
    from network.__utils__ import get_config_filename

    def console_exit():
        raise SystemExit

    config = SiteConfiguration(get_config_filename("Enter name of config file:"))
    print(term.clear, term.home)
    banner = f"""This interactive Python terminal will allow you to experiment with a SiteConfiguration object.\nThe object has been generated from the file you chose:\n\t{config.filepath}\nand you can access the methods/functions and attributes for that object using the 'config' variable.\nFor help on how to interact with object, use help(config).\n"""
    exitmsg = """"""
    shell = code.InteractiveConsole({"config": config, "exit": console_exit})
    shell.interact(banner=banner, exitmsg=exitmsg)


if __name__ == "__main__":
    while True:
        with contextlib.suppress(BaseException):
            match prompt_args():
                case 0:
                    from network import provision

                    provision.main()
                case 1:
                    get_config_gaps()
                case 2:
                    experiment()
                case _:
                    break
        with contextlib.suppress(ValueError):
            print("\n\nContinue? ('q' to quit, anything else to return):  ", end="")
            with term.cbreak():
                if term.inkey() == "q":
                    print(term.clear, term.home, end="")
                    break
