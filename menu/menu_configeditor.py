import os.path

from utility.utils_configeditor import ConfigUtilities
from videoquality import VideoQuality
from .menu_colors import *
from .menu_filenamecreator import FilenameMenu, PlaylistNameMenu


class ConfigMenu:
    """
    Contains all menus for the Config Editor
    """

    @staticmethod
    def config_header(config_path: str) -> None:
        """
        Header for config editor
        :param config_path: Direct path to the config file
        """
        print(f"\n{col('●', "red")} Welcome to the {col("Config Editor", "red")}!")
        print(f"{col('●', "magenta")} You can edit the script preferences here.")
        print(f"{col('●', "yellow")} Config path: {col(f"\'{config_path}\'", "cyan")}")

    @staticmethod
    def config_menu(problems: list) -> None:
        """
        Main menu for config editor
        :param problems: List of all problems, if any
        """
        print(f"{INFO} What would you like to do?")
        print(f"  {col('1', 'cyan')}) View Config")
        print(f"  {col('2', "cyan")}) Edit Config")

        # Display message if any problems
        print(f"  {col('3', "cyan")}) Reset to Default", end="")

        if len(problems) > 0:
            print(f" {col("[Recommended]", "yellow")}")
        else:
            print()

        print(f"  {col('4', "cyan")}) View Config Path")
        print(f"  {col('5', "cyan")}) View Problems")

        print(f"\n  {col('S', "cyan")}) Launch Downloader")
        print(f"  {col('Q', "cyan")}) Exit")

    @staticmethod
    def view_config_path(path: str) -> None:
        """
        Menu for viewing the config path
        :param path: Direct path to the config file
        """
        print(f"\n{INFO} Config path: {col(f'\'{path}\'', 'cyan')}")

    @staticmethod
    def view_config(config: dict, config_path: str) -> None:
        """
        Menu for viewing the config
        :param config: Dictionary with all preferences
        :param config_path: Direct path to the config file
        """

        config_name: str = os.path.basename(os.path.normpath(config_path))

        print(f"\n{INFO} Preferences in {col(f'\'{config_name}\'', "cyan")}:")

        for key, value in config.items():
            if key == "default_filename_format":
                # Use Filename Format display
                FilenameMenu.display_ff_full(ff_pref=value)

            elif key == "default_playlist_name_format":
                # Use Playlist Name Format display
                PlaylistNameMenu.display_pn_full(pn_pref=value)

            else:
                # Remove underscores and capitalize first letter
                t_key = key.replace("_", " ").title()

                print(f"  - {t_key}: {col(ConfigUtilities.pref_display_value(p_value=value), 'magenta')}")

    @staticmethod
    def preference_menu(config: dict, changes: dict) -> None:
        """
        List all preferences in the config file
        :param config: Dictionary with all preferences in the config
        :param changes: Dictionary of all pending changes. Can be empty if no changes
        """

        print(f"\n{INFO} Which preference do you want to change?")

        # List all preferences
        for i, (key, value) in enumerate(config.items()):

            # Remove underscores and capitalize first letter
            t_key = key.replace("_", " ").title()

            # For default filename format, show custom message
            if key == "default_filename_format":
                # Use Filename Format display
                FilenameMenu.display_ff_full(ff_pref=value, item_num=i + 1)

            elif key == "default_playlist_name_format":
                # Use Playlist Name Format display
                PlaylistNameMenu.display_pn_full(pn_pref=value, item_num=i + 1)

            else:
                print(
                    f"  {col(str(i + 1), 'cyan')}) {t_key}: "
                    f"{col(ConfigUtilities.pref_display_value(p_value=value), "magenta")} ",
                    end="")

            # Print any pending changes
            if key in changes.keys() and key != "default_filename_format":
                print(col(f"[{"None" if not isinstance(changes[key], bool) and \
                                        not changes[key] else changes[key]}]", "yellow"), end="")

            print()

        print(f"\n  {col("S", "cyan")}) Save")
        print(f"  {col("C", "cyan")}) Cancel")

    @staticmethod
    def reset_defaults(config: dict, defaults: dict) -> None:
        """
        Menu for resetting all preferences to default
        :param config: Dictionary with all preferences in the config
        :param defaults: Dictionary with all default preferences
        """

        print()

        # Print all preferences and their defaults
        for i, (key, value) in enumerate(config.items()):
            t_key = key.replace("_", " ").title()
            print(
                f"  {col(str(i + 1), "cyan")}) {t_key}: "
                f"{col(ConfigUtilities.pref_display_value(p_value=value), "magenta")} ",
                end="")

            # Display default value if config value was changed
            if key in defaults.keys() and value != defaults[key]:
                print(f"--> {col("None" if not isinstance(defaults[key], bool) and not defaults[key] else
                                 ConfigUtilities.pref_display_value(p_value=defaults[key]), "yellow")}", end="")

            print()

        print(f"\n{WARN} {col("Are you sure you want to reset all preferences to default?", "yellow")}")

    @staticmethod
    def unsaved_changes() -> None:
        """
        Message to display when trying to exit with unsaved changes
        """
        print(f"\n{WARN} {col("There are unsaved changes. Are you sure you want to cancel?", "yellow")}")

    @staticmethod
    def preference_change(p_key: str, p_value: str, p_type: str) -> None:
        """
        Menu for changing a preference
        :param p_key: Name of the preference
        :param p_value: Current value of the preference
        :param p_type: Type for the preference
        """

        # Remove underscores and capitalize first letter
        t_key = p_key.replace("_", " ").title()

        print(f"\n{ACTION} Enter a new value for {col(t_key, "magenta")}:")
        print(f"  Current Value: {col(ConfigUtilities.pref_display_value(p_value=p_value), "cyan")}")

        # Handle custom types
        if p_key == "default_video_quality":
            print(f"  Valid Video Qualities: "
                  f"{col(', '.join(list(VideoQuality.resolutions.values())), 'cyan')}")

        else:
            print(f"  Type: {col(p_type.__name__, "cyan")}")

    @staticmethod
    def preferences_saved(config_path: str) -> None:
        """
        Message to display when preferences are saved
        :param config_path: Direct path to the config file
        """
        config_name: str = os.path.basename(os.path.normpath(config_path))

        print(f"\n{SUCCESS} Preferences saved to {col(f"\'{config_name}\'", "cyan")}")

    @staticmethod
    def changes_cancelled() -> None:
        """
        Message to display when changes are cancelled
        """
        print(f"\n{ACTION} Changes cancelled.")

    @staticmethod
    def preferences_reset() -> None:
        """
        Message to display when preferences are reset
        """
        print(f"\n{ACTION} All preferences have been reset to default.")

    @staticmethod
    def reset_cancelled() -> None:
        """
        Message to display when reset is cancelled
        """
        print(f"\n{ACTION} Reset cancelled.")

    @staticmethod
    def created_config(config_path: str) -> None:
        """
        Message to display when config is created
        :param config_path: Direct path to the config file
        """
        print(f"\n{INFO} Created config file at {col(f"\'{config_path}\'", "cyan")}")

    class Messages:
        """
        Messages for Config Editor
        """

        @staticmethod
        def err_invalid_filename_formats() -> str:
            """
            String for invalid default filename formats in config
            :return: error msg
            """
            return """Invalid default filename format.

        Default filename format in config file should look like:
        default_filename_format:
          single:
          - ''
          - ''
          - ''
          playlist:
          - ''
          - ''
          - ''"""

        @staticmethod
        def err_invalid_playlist_name_format() -> str:
            """
            String for invalid default playlist name format in config
            :return: error msg
            """
            return """Invalid default playlist name format.

        Default playlist name format in config file should look like:
          default_playlist_name_format:
          - ''
          - ''
          - ''"""
