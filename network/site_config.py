"""Contains classes for parsing access point configuration files"""

import os
from . import range_string


class Config:
    """
    Simple utility class to hold configurations
    for individual wireless access points
    """

    def __init__(self, identifier: int, commands: list[str]):
        self.identifier = identifier
        self.commands = commands

    def __str__(self):
        return f"Config(AP #{self.identifier}, commands: ['{self.commands[0]}', ...])"


class SiteConfiguration:
    """Creates an object that can parse through a config file, generate a readable list of APs included in a config file (`get_range_string`), and store configs for multiple different access points"""

    configs: list[Config]

    def __init__(self, filepath: str):
        self.configs = []
        self.filepath = os.path.abspath(filepath)
        self.load_config_file(filepath)
        self.sitename = self.configs[0].commands[0][12:15]
        self.sitecode = self.configs[0].commands[1].split()[2].split(".")[1]

    def __str__(self) -> str:
        return f"{self.sitename} [{self.sitecode}] SiteConfiguration ({len(self.configs)} APs)"

    def __repr__(self) -> str:
        return f"SiteConfiguration(sitename={self.sitename}, sitecode={self.sitecode}, configs={len(self.configs)})"

    def __getitem__(self, *args):
        return self.configs.__getitem__(*args)

    def get_config_list(self):
        """Loops through each individual config block, gets the number of the AP, and adds it to a list (tuple) to be returned

        Returns:
            tuple: List of APs being configured
        """
        return tuple(x.identifier for x in self.configs)

    def get_range_string(self, with_range: bool = True, with_gaps: bool = False):
        """
            Generates a readable string that describes the ranges of APs being configured. Can be used to find gaps in config files.
            If with_range and with_gaps, returns tuple (essentially, a list) of included APs, gaps in APs
            If only with_range, returns string of included APs
            If only with_gaps, returns string of gaps in APs

            Example::
                config = SiteConfiguration("mck.txt")
                config.get_range_string()               # Returns: "1-206"
                config.get_range_string(with_gaps=True) # with_range is already True
                                                        # Returns: ("1-206", "")

                config = SiteConfiguration("wav.txt")
                config.get_range_string()                                 # Returns: "1-194, 196-279"
                config.get_range_string(with_gaps=True, with_range=False) # Returns: "195"


        Returns:
            str: Readable string of AP config ranges OR Readable string of gaps in AP config
            tuple: (String of included APs, string of excluded APs)
        """
        rs = range_string.generate_range_string(self.get_config_list(), True)
        if with_range and with_gaps:
            return rs
        elif with_range:
            return rs[0]
        elif with_gaps:
            return rs[1]

    def load_config_file(self, file_path: str):
        """Loads config file and separates each config block into individual Config objects that are stored in a list

        Args:
            file_path (str): Path to file containing configs
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

        # Check if there are any remaining commands after the last empty line
        if current_identifier is not None:
            config = Config(current_identifier, current_commands)
            self.configs.append(config)
