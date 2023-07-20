"""Contains classes for parsing access point configuration files"""

import os
from .range_string import generate_range_string


class Config:
    """
    Simple utility class to hold configurations
    for individual wireless access points
    """

    def __init__(self, identifier: int, commands: list[str]):
        """
        Initialize a Config object.

        Args:
            identifier (int): The identifier of the access point.
            commands (list[str]): The list of commands for the access point.
        """
        self.identifier = identifier
        self.commands = commands
        self.env = self.set_env()

    def __str__(self):
        """
        Return a string representation of the Config object.

        Returns:
            str: The string representation of the Config object.
        """
        return f"Config(AP #{self.identifier}, commands: ['{self.commands[0]}', ...])"

    def set_env(self):
        return {
            command[1]: command[2]
            for command in (c.split() for c in self.commands)
            if command[0] == "setenv"
        }


class SiteConfiguration:
    """
    Represents a site configuration for access points (APs).

    The `SiteConfiguration` class stores and manages configuration commands for each access point in a site.
    It allows loading configuration data from a file and provides methods to access and manipulate the configurations.

    Args:
        filename (str): The name of the file containing the site configuration.

    Attributes:
        configs (list): A list of `Config` objects representing the configurations for each access point.
    """

    configs: list[Config]

    def __init__(self, filepath: str):
        """
        Initialize a SiteConfiguration object.

        Args:
            filepath (str): The path to the configuration file.
        """
        self.configs = []
        self.filepath = os.path.abspath(filepath)
        self.load_config_file(filepath)
        self.sitename = self.configs[0].commands[0][12:15]
        self.sitecode = self.configs[0].commands[1].split()[2].split(".")[1]

    def __str__(self) -> str:
        """
        Return a string representation of the SiteConfiguration object.

        Returns:
            str: The string representation of the SiteConfiguration object.
        """
        return f"{self.sitename} [{self.sitecode}] SiteConfiguration ({len(self.configs)} APs)"

    def __repr__(self) -> str:
        """
        Return a string representation of the SiteConfiguration object.

        Returns:
            str: The string representation of the SiteConfiguration object.
        """
        return f"SiteConfiguration(sitename={self.sitename}, sitecode={self.sitecode}, configs={len(self.configs)})"

    def __getitem__(self, *args):
        """
        Get an item from the SiteConfiguration object.

        Args:
            *args: Variable length argument list.

        Returns:
            Any: The requested item from the SiteConfiguration object.
        """
        return self.configs.__getitem__(*args)

    def get_config_list(self):
        """
        Get a list of APs being configured.

        Returns:
            tuple: List of APs being configured.
        """
        return tuple(x.identifier for x in self.configs)

    def get_range_string(self, with_range: bool = True, with_gaps: bool = False):
        """
        Generate a readable string that describes the ranges of APs being configured.

        Args:
            with_range (bool, optional): Whether to include the range of APs being configured. Defaults to True.
            with_gaps (bool, optional): Whether to include the gaps in APs being configured. Defaults to False.

        Returns:
            str: Readable string of AP config ranges OR readable string of gaps in AP config
            tuple: (String of included APs, string of excluded APs)
        """
        rs = generate_range_string(self.get_config_list(), True)
        if with_range and with_gaps:
            return rs
        elif with_range:
            return rs[0]
        elif with_gaps:
            return rs[1]

    def load_config_file(self, file_path: str):
        """
        Load the config file and separate each config block into individual Config objects that are stored in a list.

        Args:
            file_path (str): The path to the file containing configs.
        """
        self.file = file_path
        with open(file_path, "r") as f:
            config_file_contents = f.read()

        config_lines = config_file_contents.split("\n")

        current_commands = []
        current_identifier = None

        for line in config_lines:
            if line.strip():
                if current_identifier is None:
                    current_identifier = int(line[-3:])
                current_commands.append(line)
            elif current_identifier is not None:
                config = Config(current_identifier, current_commands)
                self.configs.append(config)
                current_commands = []
                current_identifier = None

        if current_identifier is not None:
            config = Config(current_identifier, current_commands)
            self.configs.append(config)


def experiment():
    from .__utils__ import get_config_filename, clear_screen
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
