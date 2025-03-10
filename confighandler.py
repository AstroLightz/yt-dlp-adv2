"""
confighandler.py: Handles the config file for the script
"""

import os

from ruamel.yaml import YAML

from menu import Menu


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

            self.set_defaults()

        else:
            self.parse_config()

        self.update_config()

    def set_defaults(self) -> None:
        """
        Set default values if config file is empty.
        """

        # Copy the default config to main config file
        with open(self.config_path, "w") as f:
            self.yaml.dump(self.default_vals, stream=f)

        self.parse_config()

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

    def change_prefs(self, new_prefs: dict):
        """
        Change the value of preferences
        :param new_prefs: Dictionary of changed preferences
        """

        # Update preferences
        for key, value in new_prefs.items():
            self.config_vals[key] = value

        # Update config
        with open(self.config_path, "w") as f:
            self.yaml.dump(self.config_vals, stream=f)


class ConfigEditor:
    """
    Backend for editing the config in the script
    """

    def __init__(self):
        self.ch: ConfigHandler = ConfigHandler(file="config.yml")

        self.launch_downloader: bool = False

        # Config
        self.cur_prefs: dict = self.ch.get_config()
        self.new_prefs: dict = {}

        # Menu choices
        self.menu_choice = None
        self.p_choice = None

        # Input
        self.p_new_value = None
        self.cancel_confirm = None
        self.reset_confirm = None

        # Header is only shown once
        Menu.Config.config_header(config_path=self.ch.config_path)

        # Menu loop
        while True:
            self.main_menu()

            if self.menu_choice == '1':
                # View Config
                self.view_config()

            elif self.menu_choice == '2':
                # Edit Config
                self.edit_config()

            elif self.menu_choice == '3':
                # Reset Config
                self.reset_config()

            elif self.menu_choice == '4':
                # View Config Path
                Menu.Config.view_config_path(path=self.ch.config_path)

            elif self.menu_choice == 'S':
                # Run the Downloader
                self.launch_downloader = True
                return

            elif self.menu_choice == 'Q':
                # Exit
                Menu.Misc.exit_script()
                exit(0)

    def main_menu(self):
        Menu.gap(1)
        Menu.Config.config_menu()
        Menu.gap(1)

        # Get main menu choice
        # self.menu_choice: int = Menu.Input.get_input_num(num_entries=4, default_option=1)
        self.menu_choice: str = Menu.Input.get_input_custom(opt_range=[1, 2, 3, 4, 'S', 'Q'], default_option=1)

    def view_config(self):
        Menu.Config.view_config(config=self.cur_prefs, config_path=self.ch.config_path)

    def edit_config(self):
        while True:
            Menu.Config.preference_menu(config=self.cur_prefs, changes=self.new_prefs)
            Menu.gap(1)

            # Get preference choice
            self.p_choice: int = Menu.Input.get_input_pref(num_entries=len(self.cur_prefs))

            if self.p_choice > 0:
                # Preference selected

                # Get preference and value
                pref_key = list(self.cur_prefs.keys())[self.p_choice - 1]
                pref_val = self.cur_prefs[pref_key]

                Menu.Config.preference_change(p_key=pref_key, p_value=pref_val, p_type=type(pref_val))
                Menu.gap(1)

                # Get new value
                self.p_new_value = Menu.Input.get_input_pref_value(p_key=pref_key, p_value=pref_val)

                # Add to changes dict
                self.new_prefs[pref_key] = self.p_new_value

            elif self.p_choice == -1:
                # Save

                # Update preferences
                self.ch.change_prefs(new_prefs=self.new_prefs)

                for key, value in self.new_prefs.items():
                    self.cur_prefs[key] = value

                self.new_prefs = {}

                Menu.Config.preferences_saved(config_path=self.ch.config_path)
                break

            elif self.p_choice == -2:
                # Cancel

                # If any changes were made, prompt
                if len(self.new_prefs) > 0:
                    Menu.Config.unsaved_changes()

                    # Get confirmation
                    self.cancel_confirm = Menu.Input.get_input_bool(default_option=False)

                    # If confirmed, reset changes
                    if self.cancel_confirm:
                        Menu.Config.changes_cancelled()
                        self.new_prefs = {}
                        break

                # If no changes were made, go back
                else:
                    break

    def reset_config(self):
        # Requires confirmation

        if self.cur_prefs == self.ch.default_vals:
            # User config is already default
            Menu.Problem.Error.pref_already_default()
            return

        Menu.Config.reset_defaults(config=self.cur_prefs, defaults=self.ch.default_vals)

        # Get confirmation
        self.reset_confirm = Menu.Input.get_input_bool(default_option=False)

        # If confirmed, reset config
        if self.reset_confirm:
            self.ch.set_defaults()
            self.cur_prefs = self.ch.get_config()

            Menu.Config.preferences_reset()

        else:
            Menu.Config.reset_cancelled()
