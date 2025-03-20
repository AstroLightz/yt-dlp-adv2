"""
confighandler.py: Handles the config file for the script
"""

import os
from pathlib import PurePosixPath

from ruamel.yaml import YAML

from menu.menu_configeditor import ConfigMenu
from menu.menu_input import Input
from menu.menu_misc import MiscMenu
from menu.menu_problems import ConfigProblem
from utility.utils_configeditor import ConfigUtilities


class ConfigError(Exception):
    def __init__(self, err_code: int, msg: str):
        """
        Error in the configuration file
        :param err_code: Error code
        :param msg: Error message

        Error codes:
            - ``1`` = Empty value
            - ``2`` = Invalid value
            - ``3`` = Invalid path
            - ``4`` = Duplicate key
            - ``5`` = Malformed Config file
        """
        self.err_code = err_code
        self.msg = None

        # Default messages if not provided
        if not msg:
            if err_code == 1:
                # Empty value
                msg = "Empty value"

            elif err_code == 2:
                # Invalid value
                msg = "Invalid value"

            elif err_code == 3:
                # Invalid path
                msg = "Invalid path"

        self.msg = f"Error Code {err_code}: {msg}"

        super().__init__(self.msg)


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
            file = ConfigUtilities.CONFIG_FILENAME

        self.config_path: str = f"{self.script_dir}/{file}"

        # Get default values
        with open(self._DEFAULT_CONFIG, "r") as f:
            self.default_vals: dict = self.yaml.load(f)

        # If the file doesn't exist, create it and write defaults
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                f.write("")

            self.set_defaults()
            ConfigMenu.created_config(config_path=self.config_path)

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


class ConfigValidator:
    """
    Class for validating the config file at launch
    """

    def __init__(self, config_handler: ConfigHandler):
        self.ch: ConfigHandler = config_handler
        self.config_vals = self.ch.get_config()

        self.config_errors: list[ConfigError] = []

        # Preferences that use paths
        self.path_prefs: list[str] = [
            "video_directory",
            "audio_directory",
            "artwork_directory"
        ]

        self.validate_config()

    def validate_config(self):
        """
        Validate the config
        """

        default_vals: list = list(self.ch.default_vals.values())

        # If not a dict, raise error
        if not isinstance(self.config_vals, dict):
            err: ConfigError = ConfigError(err_code=5, msg="Malformed config file.")
            self.config_errors.append(err)

            return

        for i, (key, value) in enumerate(self.config_vals.items()):
            if key not in list(self.ch.default_vals.keys()):
                # Unknown key

                err: ConfigError = ConfigError(err_code=4, msg=f"Unknown key '{key}'")
                self.config_errors.append(err)

            if value is None:
                # Value is None

                err: ConfigError = ConfigError(err_code=1, msg=f"'{key}': Value cannot be empty or null.")
                self.config_errors.append(err)

            if not isinstance(value, type(default_vals[i])):
                # Type does not match

                err: ConfigError = ConfigError(err_code=2,
                                               msg=f"'{key}': Value must be type '{type(default_vals[i]).__name__}'"
                                                   f"\n      Current value: '{value}'"
                                                   f"\n      Current type: '{type(value).__name__}'")
                self.config_errors.append(err)

            if key == "default_filename_format":
                # Validate filename formats

                self.validate_fileformats(key=key)

            if isinstance(value, str) and key in self.path_prefs:
                # Validate path

                self.validate_path(key=key, value=value)

    def validate_fileformats(self, key: str):
        """
        Validate default filename formats
        """

        try:
            default_formats = self.ch.config_vals[key]

            # Not a dictionary
            if not isinstance(default_formats, dict):
                raise AttributeError

            # dict key values are not list[str]
            for k, v in default_formats.items():
                if not isinstance(v, list):
                    raise AttributeError

                elif not all(isinstance(i, str) for i in v):
                    raise AttributeError

                # dict keys must be "single" and "playlist"
                elif k not in ["single", "playlist"]:
                    raise AttributeError

        except AttributeError:
            err: ConfigError = ConfigError(err_code=2,
                                           msg=f"'{key}': {ConfigMenu.Messages.err_invalid_filename_formats()}")
            self.config_errors.append(err)

    def validate_path(self, key: str, value: str):
        """
        Validate any preferences that are paths
        """

        if key in self.path_prefs:
            # Ensure path is valid

            # Ensure path is Unix-based
            try:
                posix_path: PurePosixPath = PurePosixPath(value)

            except Exception as e:
                err: ConfigError = ConfigError(err_code=2, msg=f"'{key}': Path error: {e}")
                self.config_errors.append(err)

                return

            if not isinstance(value, str) or not value:
                # Empty path

                err: ConfigError = ConfigError(err_code=1, msg=f"'{key}': Path cannot be empty")
                self.config_errors.append(err)

                return

            if "\0" in value:
                # No null characters allowed

                err: ConfigError = ConfigError(err_code=2, msg=f"'{key}': Path cannot contain null characters")
                self.config_errors.append(err)

            if value[0] != '/' and value[0] != '~':
                # No relative paths allowed

                err: ConfigError = ConfigError(err_code=3,
                                               msg=f"'{key}': Path must be valid and absolute: "
                                                   f"Must begin with / or ~"
                                                   f"\n      Current path: '{value}'")
                self.config_errors.append(err)

            # Path can contain periods if it ends with a '/'
            if posix_path.name and not value.endswith('/') and posix_path.suffix:
                # Path is a file

                err: ConfigError = ConfigError(err_code=3,
                                               msg=f"'{key}': Path cannot be a file"
                                                   f"\n      If this was intended to be a directory, "
                                                   f"Add a '/' to the end of the path"
                                                   f"\n      Current path: '{value}'")
                self.config_errors.append(err)


class ConfigEditor:
    """
    Backend for editing the config in the script
    """

    def __init__(self):
        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)

        # Validate config
        self.errors: list[ConfigError] = ConfigValidator(config_handler=self.ch).config_errors

        self.launch_downloader: bool = False

        self.menu_options: list = [1, 2, 3, 4, 5, 'S', 'Q']

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
        ConfigMenu.config_header(config_path=self.ch.config_path)

        # Display errors if any
        if len(self.errors) > 0:
            ConfigProblem.Warning.config_problems(e=self.errors)

        else:
            MiscMenu.gap(2)

        # Menu loop
        while True:

            # Force reset the config file if it is malformed
            if len(self.errors) > 0 and self.errors[0].err_code == 5:
                ConfigProblem.Warning.config_force_reset()
                self.reset_config()

            else:
                self.main_menu()

                match self.menu_choice:
                    case '1':
                        # View Config
                        try:
                            self.view_config()

                        except (KeyError, TypeError, AttributeError, ValueError, IndexError):
                            ConfigProblem.Error.config_menu_error()
                            continue

                    case '2':
                        # Edit Config
                        try:
                            self.edit_config()

                        except (KeyError, TypeError, AttributeError, ValueError, IndexError):
                            ConfigProblem.Error.config_menu_error()
                            continue

                    case '3':
                        # Reset Config
                        self.reset_config()

                    case '4':
                        # View Config Path
                        ConfigMenu.view_config_path(path=self.ch.config_path)

                    case '5':
                        # View Config Problems

                        if len(self.errors) > 0:
                            ConfigProblem.Warning.config_problems(e=self.errors)

                        else:
                            ConfigProblem.Success.config_no_problems()

                    case 'S':
                        # Run the Downloader
                        self.launch_downloader = True
                        return

                    case 'Q':
                        # Exit
                        MiscMenu.exit_script()
                        exit(0)

    def main_menu(self):
        MiscMenu.gap(1)
        ConfigMenu.config_menu(problems=self.errors)
        MiscMenu.gap(1)

        # Get main menu choice
        # self.menu_choice: int = Menu.Input.get_input_num(num_entries=4, default_option=1)
        self.menu_choice: str = Input.String.get_input_custom(opt_range=self.menu_options, default_option=1)

    def view_config(self):
        ConfigMenu.view_config(config=self.cur_prefs, config_path=self.ch.config_path)

    def edit_config(self):
        from filenamecreator import FilenameCreator

        while True:
            ConfigMenu.preference_menu(config=self.cur_prefs, changes=self.new_prefs)
            MiscMenu.gap(1)

            # Get preference choice
            self.p_choice: int = Input.Preference.get_input_pref(num_entries=len(self.cur_prefs))

            if self.p_choice > 0:
                # Preference selected

                # Get preference and value
                pref_key = list(self.cur_prefs.keys())[self.p_choice - 1]
                pref_val = self.cur_prefs[pref_key]
                def_val = list(self.ch.default_vals.values())[self.p_choice - 1]

                # Use Filename Creator if editing default filename format
                if pref_key == "default_filename_format":
                    FilenameCreator(dwn_mode=-1)

                    # Reload preferences
                    self.ch = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
                    self.cur_prefs = self.ch.get_config()
                    break

                ConfigMenu.preference_change(p_key=pref_key, p_value=pref_val, p_type=type(def_val))
                MiscMenu.gap(1)

                # Get new value
                self.p_new_value = Input.Preference.get_input_pref_value(p_key=pref_key, p_value=pref_val,
                                                                         d_value=def_val)

                # Add to changes dict
                self.new_prefs[pref_key] = self.p_new_value

            elif self.p_choice == -1:
                # Save

                # Update preferences
                self.ch.change_prefs(new_prefs=self.new_prefs)

                for key, value in self.new_prefs.items():
                    self.cur_prefs[key] = value

                self.new_prefs = {}

                # Check for errors
                self.errors = ConfigValidator(config_handler=self.ch).config_errors

                ConfigMenu.preferences_saved(config_path=self.ch.config_path)
                break

            elif self.p_choice == -2:
                # Cancel

                # If any changes were made, prompt
                if len(self.new_prefs) > 0:
                    ConfigMenu.unsaved_changes()

                    # Get confirmation
                    self.cancel_confirm = Input.Boolean.get_input_bool(default_option=False)

                    # If confirmed, reset changes
                    if self.cancel_confirm:
                        ConfigMenu.changes_cancelled()
                        self.new_prefs = {}
                        break

                # If no changes were made, go back
                else:
                    break

    def reset_config(self):
        # Requires confirmation

        try:
            if self.cur_prefs == self.ch.default_vals:
                # User config is already default
                ConfigProblem.Error.pref_already_default()
                return

            # Skip confirmation if config file is deformed
            if len(self.errors) > 0 and self.errors[0].err_code == 5:
                self.reset_confirm = True

            else:
                ConfigMenu.reset_defaults(config=self.cur_prefs, defaults=self.ch.default_vals)

                # Get confirmation
                self.reset_confirm = Input.Boolean.get_input_bool(default_option=False)

        except (KeyError, TypeError, AttributeError, ValueError, IndexError):
            # Skip confirmation if an error prevents confirmation
            self.reset_confirm = True

        # If confirmed, reset config
        if self.reset_confirm:
            self.ch.set_defaults()

            # Reload preferences
            self.ch = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
            self.cur_prefs = self.ch.get_config()

            # Check for errors
            self.errors = ConfigValidator(config_handler=self.ch).config_errors

            ConfigMenu.preferences_reset()

        else:
            ConfigMenu.reset_cancelled()
