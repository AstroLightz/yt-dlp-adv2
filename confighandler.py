"""
confighandler.py: Handles the config file for the script
"""
from ruamel.yaml import YAML
import os


class ConfigHandler:
    """
    Handles the config file for the script
    """

    def __init__(self, file: str):
        """
        :param file: Direct file path for the config
        """

        self.yaml = YAML(typ="rt")

        self.config_vals = None
        self.default_vals = None

        # Get script directory
        self.script_dir: str = os.path.dirname(os.path.realpath(__file__))

        self._DEFAULT_CONFIG: str = f"{self.script_dir}/.default_config.yml"

        # Set default config path if not provided
        if not file:
            file = "config.yml"

        self.config_path: str = f"{self.script_dir}/{file}"

        # Get default values
        with open(self._DEFAULT_CONFIG, "r") as f:
            self.default_vals: dict = self.yaml.load(f)

        # If the file doesn't exist, create it and write defaults
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                f.write("")

            self._set_defaults()

        self.parse_config()
        self.update_config()

    def _set_defaults(self) -> None:
        """
        Set default values if config file is empty.
        """

        # Copy the default config to main config file
        with open(self.config_path, "w") as f:
            self.yaml.dump(self.default_vals, stream=f)

    def update_config(self) -> None:
        """
        Update config file if new values are added to the default. Keeps values set by user
        """

        # If the config file is empty, copy default values
        if self.config_vals is None:
            with open(self.config_path, "w") as f:
                self.yaml.dump(self.default_vals, stream=f)

        # Update user config if default has more entries
        elif len(self.default_vals) > len(self.config_vals):

            # Get separate defaults so main one is not modified
            with open(self._DEFAULT_CONFIG, "r") as f:
                new_config: dict = self.yaml.load(f)

            # Write user config values to default dict
            for key, value in self.config_vals.items():
                new_config[key] = value

            # Write default dict to config file
            with open(self.config_path, "w") as f:
                self.yaml.dump(new_config, stream=f)

    def parse_config(self):
        """
        Parse the config file to the ConfigHandler
        """

        with open(self.config_path, "r") as f:
            self.config_vals = self.yaml.load(f)

    def get_config(self) -> dict:
        """
        Get the config file as a dict
        :return: Dictionary of all options in the config
        """

        # If user config is empty, return defaults
        return self.config_vals if self.config_vals is not None else self.default_vals
