import os.path
from typing import Any

from termcolor import colored as col

from utilities import Utilities
from videoquality import VideoQuality

# Message types
SUCCESS: str = f"{col('✔', "green")}"
FAIL: str = f"{col('✘', "red")}"
INFO: str = f"{col('?', "yellow")}"
WARN: str = f"{col('⚠️', "yellow")}"
ACTION: str = f"{col('➜', "blue")}"

# ANSI Codes for input
CYAN: str = "\033[36m"
RESET: str = "\033[0m"


class Menu:
    """
    Contains all menus for the program
    """

    class Config:
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
                    # Show custom display
                    Menu.FilenameFormat.display_ff_full(ff_pref=value)

                else:
                    # Remove underscores and capitalize first letter
                    t_key = key.replace("_", " ").title()

                    print(f"  - {t_key}: {col(Utilities.pref_display_value(p_value=value), 'magenta')}")

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
                    # print(f"  {col(str(i + 1), 'cyan')}) {t_key}: "
                    #       f"{col("Edit with Filename Creator", "yellow")} ", end="")
                    Menu.FilenameFormat.display_ff_full(ff_pref=value, item_num=i + 1)

                else:
                    print(
                        f"  {col(str(i + 1), 'cyan')}) {t_key}: "
                        f"{col(Utilities.pref_display_value(p_value=value), "magenta")} ",
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
                    f"{col(Utilities.pref_display_value(p_value=value), "magenta")} ",
                    end="")

                # Display default value if config value was changed
                if key in defaults.keys() and value != defaults[key]:
                    print(f"--> {col("None" if not isinstance(defaults[key], bool) and not defaults[key] else
                                     Utilities.pref_display_value(p_value=defaults[key]), "yellow")}", end="")

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
            print(f"  Current Value: {col(Utilities.pref_display_value(p_value=p_value), "cyan")}")

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

    class Arguments:
        """
        Contains all menus for arguments passed to the script
        """

        @staticmethod
        def help_menu() -> None:
            """
            Displays help menu
            """
            print(f"{INFO} Usage: main.py {col("[options]", "cyan")}"
                  f"\n\nOptions:"
                  f"\n{col("-h, --help", "cyan")}: Show this help message."
                  f"\n{col("-v, --version", "cyan")}: Show script version."
                  f"\n{col("-c, --config", "cyan")}: Open the Config Editor."
                  f"\n{col("-f, --filename-creator", "cyan")}: Open the Filename Creator.")

        @staticmethod
        def show_version(v: str) -> None:
            """
            Displays script version
            :param v: Version string from main
            """
            print(f"{INFO} Script version: {col(v, 'cyan')}")

        @staticmethod
        def show_commits(g_commits: str) -> None:
            """
            Displays GitHub link for commits/updates
            :param g_commits: GitHub commits link
            """
            print(f"{INFO} GitHub commits: {col(g_commits, 'cyan')}")

        @staticmethod
        def defaults_bypassed() -> None:
            """
            Message to display when default preferences are bypassed
            """
            print(f"\n{INFO} Default preferences will be ignored for this session.")

    class Misc:
        """
        Miscellaneous menus/messages that don't fit anywhere else
        """

        @staticmethod
        def exit_script() -> None:
            """
            Message when exiting the script, such as using CTRL+C
            """
            print(f"\n{ACTION} Exiting script...")

        @staticmethod
        def download_aborted() -> None:
            """
            Message when a download is aborted (Choosing N on the confirmation menu)
            """
            print(f"\n{WARN} {col("Download aborted.", "yellow")}")

    class Input:
        """
        Contains all input prompts and input validation
        """

        @staticmethod
        def get_input_format() -> str:
            """
            Get input for Advanced filename format
            :return: yt-dlp filename format
            """

            while True:
                try:
                    ytdlp_format: str = input(f"> {CYAN}")

                    # Reset ANSI codes
                    print(RESET, end="")

                    if "%(" not in ytdlp_format and ")s" not in ytdlp_format:
                        raise ValueError

                    return ytdlp_format

                except ValueError:
                    print(f"\n{FAIL} {col("Invalid yt-dlp format. "
                                          "Make sure to include \'%(\' and \')s\' for special names.", "red")}")

        @staticmethod
        def get_input_custom(opt_range: list[int | str], default_option: int | str = 1,
                             no_default: bool = False, list_options: bool = True,
                             dynamic_options: bool = False) -> str:
            """
            Custom Input system. Provide the options range and (optionally) the default option
            :param opt_range: List of integers representing the options. Order in the list will be used in display.
            :param default_option: Default option
            :param no_default: If True, no default option
            :param list_options: If True, list available options
            :param dynamic_options: If True, uses the length of the options range to display options. Otherwise,
            uses the options list directly
            :return: The selected option
            """

            # Get options
            if dynamic_options:
                options_list, max_entries_str = Utilities.input_get_options(entries=len(opt_range))

            else:
                options_list: str = '['

                for opt in opt_range:
                    if opt != opt_range[-1]:
                        options_list += f"{opt}/"
                    else:
                        options_list += f"{opt}"

                options_list += "]"
                max_entries_str = options_list[-1]

            while True:
                try:
                    if no_default and list_options:
                        # > [options]:

                        choice = input(f"> {col(options_list, "magenta")}: ")

                    elif no_default:
                        # >

                        choice = input("> ")

                    elif list_options:
                        # > [options] (default):

                        choice = input(f"> {col(options_list, "magenta")} "
                                       f"{col(f"({default_option})", "cyan")}: ") or str(default_option)

                    else:
                        # > (default):

                        choice = input(f"> {col(f"({default_option})", "cyan")}: ") or str(default_option)

                    # Handle integers
                    if choice.isnumeric():
                        if int(choice) not in [int(opt) if isinstance(opt, str) and opt.isnumeric() else opt for opt in
                                               opt_range]:
                            raise ValueError

                    else:
                        if choice.upper() not in [opt.upper() if isinstance(opt, str) else opt for opt in opt_range]:
                            raise ValueError

                    return choice.upper() if choice.isalpha() else choice

                except ValueError:
                    if dynamic_options and len(opt_range) > 10:
                        print(
                            f"\n{FAIL} {col(f"Invalid input. Please enter an integer or letter between 1-0 and "
                                            f"{f"A-{max_entries_str}" if len(opt_range) > 11 else \
                                                max_entries_str}.", "red")}")

                    elif dynamic_options:
                        print(
                            f"\n{FAIL} {col(f"Invalid input. Please enter an integer between 1 and {"0" \
                                if len(opt_range) > 9 else len(opt_range)}.", "red")}")

                    else:
                        print(
                            f"\n{FAIL} {col(f"Invalid input. Please enter a valid option: "
                                            f"{opt_range}", "red")}")

        @staticmethod
        def get_input_pref_value(p_key: str, p_value: Any, d_value: Any) -> Any:
            """
            Special Input for the config editor. Get the new value for a preference
            :param p_key: Key of the preference. Used for overriding certain value types
            :param p_value: Current value of the preference
            :param d_value: Default value of the preference
            :return: Returns a value for the selected preference
            """

            # Get required type
            req_type = type(d_value)

            while True:
                new_value = input(f"> {CYAN}")

                # Reset ANSI codes
                print(RESET, end="")

                try:
                    # Try to convert the input to the same type as the preference
                    if p_key == "default_video_quality":
                        # For Video Quality, ensure input is a valid resolution

                        try:
                            if new_value:
                                new_value = VideoQuality(value=new_value).quality

                            else:
                                # Allow setting default to null
                                new_value = ""

                        except VideoQuality.InvalidQuality:
                            print(f"\n{FAIL} Invalid Video Quality: {col(new_value, 'cyan')}")
                            print(
                                f"  Valid Video Qualities: "
                                f"{col(', '.join(list(VideoQuality.resolutions.values())), 'cyan')}\n")
                            continue

                    elif isinstance(d_value, bool):
                        # Allow case-insensitive input
                        if new_value.lower() in ["true", "false"]:
                            new_value = (new_value.lower() == "true")

                        else:
                            raise ValueError

                    elif isinstance(d_value, int):
                        new_value = int(new_value)

                    elif isinstance(d_value, float):
                        new_value = float(new_value)

                    elif isinstance(d_value, str):
                        new_value = str(new_value)

                    else:
                        # If the type is not supported, display error
                        print(f"{FAIL} Unsupported Type: {col(req_type.__name__, 'red')}")
                        continue

                    # Display error if new value is same as current value
                    if new_value == p_value:
                        print(f"\n{FAIL} {col("New value cannot be the same as the current value.", "red")}")

                    else:
                        return new_value

                except ValueError:
                    print(f"\n{FAIL} Invalid Input: {col(new_value, "cyan")}")
                    print(f"  Expected Type: {col(req_type.__name__, "cyan")}\n")

        @staticmethod
        def get_input_pref(num_entries: int) -> int:
            """
            Get the preference from the user
            :param num_entries: Number of entries in the menu
            :return: Preference choice
            """

            # Create options list string
            options_list: str = "["

            for i in range(num_entries):
                if i != num_entries - 1:
                    options_list += f"{i + 1}/"
                else:
                    options_list += f"{i + 1}"

            # Add save and cancel
            options_list += "/S/C"

            options_list += "]"

            while True:
                try:
                    choice = input(f"> {col(options_list, "magenta")}: ")

                    # If choice is not save or cancel
                    if choice.upper() != "S" and choice.upper() != "C":
                        choice = int(choice)

                        if choice < 1 or choice > num_entries:
                            raise ValueError

                        return choice

                    elif choice.upper() == "S":
                        # Save and exit
                        return -1

                    elif choice.upper() == "C":
                        # Cancel
                        return -2

                    else:
                        raise ValueError

                except ValueError:
                    print(
                        f"\n{FAIL} {col(f"Invalid input. Please enter a value "
                                        f"between 1 and {num_entries}, or S for Save or C for Cancel.", "red")}")

        @staticmethod
        def get_input_num(num_entries: int = 3, default_option: int = 1, no_default: bool = False) -> int:
            """
            Gets a numeric input from the user. If num_entries is greater than 8,
            use `Menu.Input.get_input_long()` instead.
            :param default_option: The default option to select
            :param num_entries: Number of entries in the menu. Must be at least 2
            :param no_default: If True, will require the user to select an option
            :return: The selected option
            """

            # Create options list string
            options_list: str = "["

            for i in range(num_entries):
                if i != num_entries - 1:
                    options_list += f"{i + 1}/"
                else:
                    options_list += f"{i + 1}"

            options_list += "]"

            while True:
                try:
                    if no_default:
                        choice: int = int(
                            input(f"> {col(options_list, "magenta")}: "))

                    else:
                        choice: int = int(
                            input(
                                f"> {col(options_list, "magenta")} "
                                f"{col(f"({default_option})", "cyan")}: ") or default_option)

                    if choice < 1 or choice > num_entries:
                        raise ValueError

                    return choice

                except ValueError:
                    print(
                        f"\n{FAIL} {col(f"Invalid input. Please enter an integer between 1 and "
                                        f"{num_entries}.", "red")}")

        @staticmethod
        def get_input_long(num_entries: int = 3, default_option: int = 1) -> int:
            """
            Similar to get_input_num, but after 9 entries, the list goes to 0, then A, B, C, etc.
            :param default_option: The default option to select
            :param num_entries: Number of entries in the menu. Must be at least 2
            :return: The selected option
            """

            # Get options
            options_list, max_entries_str = Utilities.input_get_options(entries=num_entries)

            # # Create options list string
            # options_list: str = "["
            #
            # # Calculate the max entries string
            # if num_entries > 10:
            #     # User chars
            #     max_entries_str: str = chr(54 + num_entries)
            #
            # elif num_entries > 9:
            #     # 10 entries: use 0
            #     max_entries_str: str = "0"
            #
            # else:
            #     # 1-9 entries: use the number
            #     max_entries_str = str(num_entries)
            #
            # for i in range(num_entries):
            #     if i != num_entries - 1:
            #
            #         # If the number is less than 10, add it to the list
            #         if i < 9:
            #             options_list += f"{i + 1}/"
            #         # If the number is 10, add 0 to the list
            #         elif i == 9:
            #             options_list += "0/"
            #
            #         # If the number is greater than 10, add the letter to the list (A, B, C, etc.)
            #         else:
            #             options_list += f"{chr(55 + i)}/"
            #
            #     else:
            #
            #         if i < 9:
            #             options_list += f"{i + 1}"
            #         elif i == 9:
            #             options_list += "0"
            #         else:
            #             options_list += f"{chr(55 + i)}"
            #
            # options_list += "]"

            while True:
                try:
                    choice_str: str = (input(
                        f"> {col(options_list, "magenta")} "
                        f"{col(f"({default_option})", "cyan")}: ").upper()
                                       or default_option)

                    if num_entries > 10:

                        # Convert 0 to 10 and Letters to 10 + LTR
                        if choice_str == "0":
                            choice: int = 10
                        elif choice_str.isalpha():
                            choice: int = ord(choice_str.upper()) - 54
                        else:
                            choice: int = int(choice_str)

                    elif num_entries > 9:

                        # Convert 0 to 10
                        if choice_str == "0":
                            choice: int = 10
                        else:
                            choice: int = int(choice_str)

                    else:

                        # Convert to num
                        choice: int = int(choice_str)

                    if choice < 1 or choice > num_entries:
                        raise ValueError

                    return choice

                except ValueError:
                    if num_entries > 10:
                        print(
                            f"\n{FAIL} {col(f"Invalid input. Please enter an integer or letter between 1-0 and "
                                            f"{f"A-{max_entries_str}" if num_entries > 11 else \
                                                max_entries_str}.", "red")}")

                    else:
                        print(
                            f"\n{FAIL} {col(f"Invalid input. Please enter an integer between 1 and {"0" \
                                if num_entries > 9 else num_entries}.", "red")}")

        @staticmethod
        def get_input_bool(default_option: bool) -> bool:
            """
            Get a boolean input from the user (Y or N)
            :param default_option: The default option to select
            :return: The selected option as a boolean
            """
            while True:
                try:
                    choice: str = input(
                        f"> {col(f"[{'Y' if default_option else 'y'}/"
                                 f"{'N' if not default_option else 'n'}]", "magenta")}: "
                    ).lower()

                    if choice not in ["y", "n"] and choice != "":
                        raise ValueError
                    elif choice == "":
                        return default_option

                    # Returns true if choice is "y", false if choice is "n"
                    return choice == "y"

                except ValueError:
                    print(
                        f"\n{FAIL} {col("Invalid input. Please enter 'Y' or 'N'.", "red")}")

        @staticmethod
        def get_input_url() -> str:
            """
            Get the URL of the item
            :return: The URL of the item
            """
            allowed: list[str] = ["www.youtube.com", "youtube.com", "www.youtu.be", "youtu.be"]
            is_allowed: bool = True

            while True:
                try:
                    url: str = input(f"> {CYAN}")

                    # Reset ANSI codes
                    print(RESET, end="")

                    # Handle Invalid URLs
                    if ("https://" not in url and "http://" not in url) or url == "":
                        raise ValueError

                    # Handle non-YouTube URLs
                    is_allowed = Utilities.is_allowed_url(url=url, allowed_urls=allowed)

                    if not is_allowed:
                        raise ValueError

                    return url

                except ValueError:
                    if not is_allowed:
                        Menu.Problem.Error.not_youtube_url(allowed_urls=allowed)

                    else:
                        Menu.Problem.Error.invalid_url()

    @staticmethod
    def gap(length: int = 3):
        """
        Creates a gap between lines
        :param length: Number of lines between messages
        """
        print("\n" * length, end="")

    class Main:
        """
        Contains all menus that are not specific to any particular download type
        """

        @staticmethod
        def program_header(v: str) -> None:
            """
            Header to be displayed when the script is launched
            :param v: The version of the script. If provided, it will be displayed
            """

            print(f"\nWelcome to {col("YouTube Downloader: Advanced 2.0", "red")}!")

            if v:
                Menu.Arguments.show_version(v=v)

            print(
                f"\n{col('●', "red")} This is a Python program that simplifies the use of the "
                f"{col("yt-dlp", "red")} tool "
                f"({col("https://github.com/yt-dlp/yt-dlp", "cyan")}).")
            print(
                f"{col('●', "red")} It provides a menu-driven interface to help you "
                f"download videos, audio, and thumbnails from YouTube.")
            print(
                f"{col('●', "red")} You can customize download options and formats without "
                f"needing to remember complex yt-dlp arguments.")
            print(f"{col('●', "red")} The program supports downloading entire playlists or single items.")
            print(f"{col('●', "red")} It also offers detailed feedback on the download "
                  "status and file sizes.\n")
            print(
                f"{col('●', "magenta")} This is a remake of the original "
                f"{col('yt-dlp-adv', 'cyan')}, "
                f"now with new features and quality-of-life improvements.")
            print(f"{col('●', "yellow")} Script made by {col("AstroLightz", "cyan")}. "
                  f"I hope you enjoy!")

        @staticmethod
        def main_menu() -> None:
            """
            Displays list of download types
            """
            print(f"\n{INFO} What would you like to download?")
            print(f"  {col('1', "cyan")}) Videos")
            print(f"  {col('2', "cyan")}) Audio")
            print(f"  {col('3', "cyan")}) Thumbnails")

        @staticmethod
        def item_count() -> None:
            """
            Get if item is a playlist or single item
            """
            print(f"\n{INFO} Is it a playlist or a single item?")
            print(f"  {col('1', "cyan")}) Single Item")
            print(f"  {col('2', "cyan")}) Playlist")

        @staticmethod
        def get_url() -> None:
            """
            Get the URL of the item
            """
            print(f"\n{INFO} Enter the YouTube URL:")

        @staticmethod
        def confirmation_screen(dwn_type: int, file_format: int, item_count: int, ff_mode: int,
                                filename_format: list[str], video_quality: str or None) -> None:
            """
            Display a confirmation screen with all chosen options
            :param dwn_type: Download type
            :param file_format: File format
            :param item_count: Item count (Single Item/Playlist)
            :param ff_mode: Type of filename format
            :param filename_format: Filename format list
            :param video_quality: Video quality
            """

            # Get names of download choices
            v_dwn_type: str = Utilities.get_download_type(dwn_type=dwn_type)
            v_file_format: str = Utilities.get_file_format(file_format=file_format, dwn_type=dwn_type)
            v_item_count: str = Utilities.get_download_mode(item_count=item_count)
            v_filename_format: str = Utilities.get_filename_format(item_count=item_count, ff_mode=ff_mode,
                                                                   filename_format=filename_format)

            # Display confirmation screen
            print(f"\n{INFO} Chosen Options:"
                  f"\n - Download Type: {col(f"'{v_dwn_type}'", "cyan")}"
                  f"\n - File Format: {col(f"'{v_file_format}'", "cyan")}"
                  f"\n - Mode: {col(f"'{v_item_count}'", "cyan")}", end="")

            # Hide filename format for Artwork
            print(f"\n - Filename Format: {col(f"'{v_filename_format}'", "cyan")}" \
                      if dwn_type != 3 else "", end="")

            # Show video quality for Videos
            print(f"\n - Video Quality: {col(f"'{video_quality}'", "cyan")}" \
                      if video_quality else "", end="")

            print("\n")
            print(f"{INFO} Proceed with the download?")

    class FilenameFormat:
        """
        Contains all menus/messages regarding filename formats and the Filename Creator
        """

        @staticmethod
        def format_mode() -> None:
            """
            Menu to choose which mode to use: Presets or Custom
            """
            print(f"\n{INFO} What type of filename format do you want to use?")
            print(f"  {col('1', "cyan")}) Presets")
            print(f"  {col('2', "cyan")}) Custom")

        @staticmethod
        def default_format(default_format: str) -> None:
            """
            Message to display in Downloader when using a default format
            :param default_format: Default filename format
            """
            print(f"\n{INFO} Using default filename format: {col(f"\'{default_format}\'", "cyan")}")

        @staticmethod
        def display_ff_full(ff_pref: dict[str, list[str]], item_num: int = 0) -> None:
            """
            Display full filename format tree. Used for Config Editor
            :param ff_pref: Default filename format preference
            :param item_num: Item number in Edit Config to display as #). Uses - if 0
            """

            single_vals: list[str] = ff_pref[list(ff_pref.keys())[0]]
            playlist_vals: list[str] = ff_pref[list(ff_pref.keys())[1]]

            # Item num display
            print(f"  {col(item_num, "cyan")}) " if item_num != 0 else "  - ", end="")

            # Display edit message if item num is set
            print(f"Default Filename Format: "
                  f"{col("Edit with Filename Creator", "cyan") if item_num != 0 else ''}")

            print("    * Single Item:")

            print(f"        Display Format:  {col(f"\'{single_vals[0]}\'", "magenta")}")
            print(f"        f-string Format: {col(f"\'{single_vals[1]}\'", "magenta")}")
            print(f"        yt-dlp Format:   {col(f"\'{single_vals[2]}\'", "magenta")}")

            print("    * Playlist:")

            print(f"        Display Format:  {col(f"\'{playlist_vals[0]}\'", "magenta")}")
            print(f"        f-string Format: {col(f"\'{playlist_vals[1]}\'", "magenta")}")
            print(f"        yt-dlp Format:   {col(f"\'{playlist_vals[2]}\'", "magenta")}", end="")

            if item_num == 0:
                print()

        class Presets:
            """
            Filename format preset menus/messages
            """

            @staticmethod
            def preset_menu(presets: list[str]) -> None:
                """
                Get the format for the filename
                :param presets: List of presets
                """
                print(f"\n{INFO} What format do you want the filenames to be?")

                for i, p in enumerate(presets):
                    print(f"  {col(str(i + 1), 'cyan')}) {p}")

        class Custom:
            """
            Filename format custom menus/messages
            """

            @staticmethod
            def fc_header(dwn_mode: int, default_format: str = "") -> None:
                """
                Display header for Filename Creator
                :param dwn_mode: Download mode
                :param default_format: Default filename format if it exists
                """
                print(f"\n{col('●', "red")} Welcome to the {col("Filename Creator", "red")}!")
                print(f"{col('●', "magenta")} Construct your own filename format for you downloads.")

                print(f"{col('●', "yellow")} Download Mode: "
                      f"{col("Single Item" if dwn_mode == 1 else "Playlist", "cyan")}")

                # Display default if it exists
                if default_format:
                    print(f"{col('●', "yellow")} Default Format: {col(
                        "None" if not default_format else f"\'{default_format}\'", "cyan")}")

            @staticmethod
            def fc_mode() -> None:
                """
                Menu to choose which mode for Filename Creator
                """
                print(f"\n{INFO} What mode do you want to use?")
                print(f"  {col('1', "cyan")}) Simple")
                print(f"  {col('2', "cyan")}) Advanced")

            @staticmethod
            def fc_dwn_mode(dwn_mode: int, defaults: list[str]) -> None:
                """
                Menu to get which Download mode to edit for when using FC through argument
                :param dwn_mode: Download mode
                :param defaults: List of default formats for each download mode
                """

                # Custom header for edit mode
                print(f"\n{col('●', "red")} {col("[EDIT MODE]", "yellow")}: "
                      "Edit default filename formats for each download mode.")
                print(f"\n{col('●', "magenta")} Current Defaults:")
                print(f"{col('●', "yellow")} Single Item: {col(
                    "None" if not defaults[0] else f"\'{defaults[0]}\'", "cyan")}")

                print(f"{col('●', "yellow")} Playlist: {col(
                    "None" if not defaults[1] else f"\'{defaults[1]}\'", "cyan")}")

                print(f"\n{INFO} What download mode do you want to use?")
                print(f"  {col('1', 'cyan')}) Single Item")
                print(f"  {col('2', 'cyan')}) Playlist")
                print(f"  {col('3', 'cyan')}) Clear Defaults")

                # Don't show launch downloader if coming from Config Editor
                if dwn_mode != -1:
                    print(f"\n  {col('S', "cyan")}) Launch Downloader")

                else:
                    print()

                print(f"  {col('Q', 'cyan')}) Exit")

            @staticmethod
            def fc_clear_confirm() -> None:
                """
                Prompt for confirmation to clear defaults for Single Item and Playlist default FFs
                """
                print(f"\n{WARN} {col("Are you sure you want to set the defaults to None?", "yellow")}")

            @staticmethod
            def fc_confirm(cur_format: str) -> None:
                """
                Menu to confirm the filename format in
                :param cur_format: Filename format
                """
                print(f"\n{INFO} Current Format: {col(
                    "None" if not cur_format else f"\'{cur_format}\'", 'cyan')}")

                print("  Is this correct?")

            @staticmethod
            def fc_make_default(cur_format: str, dwn_mode: int, default_format: str = "") -> None:
                """
                Prompt for setting default if it doesn't exist
                :param cur_format: Current format
                :param dwn_mode: Download mode
                :param default_format: Default format saved if provided
                """
                dwn_txt: str = "Single Item" if dwn_mode == 1 else "Playlist"

                if not default_format:
                    print(f"\n{INFO} No default is set in the config for {col(dwn_txt, "cyan")}.")

                else:
                    print(f"\n{INFO} Current default is {col(f"\'{default_format}\'", "cyan")}.")

                # If current format is empty and default is set, prompt for clearing default
                if not cur_format and default_format:
                    print("  Do you want to remove the default format?")

                else:
                    print(f"  Do you want to set it to {col(f"\'{cur_format}\'", "cyan")}?")

            @staticmethod
            def fc_simple_options(cur_format: str, format_parts: dict[str, list[str]],
                                  added: list[int], msg: str = "") -> None:
                """
                Display all available parts for Filename Creator
                :param cur_format: Current filename format
                :param format_parts: Dictionary of part names: yt-dlp part format
                :param added: List of added parts by their number
                :param msg: Message to display, if any
                """

                # Get options
                options: list[str] = Utilities.menu_get_options(entries=len(format_parts))

                print(f"\n{INFO} The following format parts are available:")

                # Display format parts in a table
                for i, p_name in enumerate(format_parts.keys()):

                    # Write to left column
                    if i % 2 == 0:
                        if i + 1 in added:
                            print(f"  {col(f"{options[i]}) {f"\'{p_name}\'":<25}", "red")}", end="")

                        else:
                            print(f"  {col(options[i], "cyan")}) {f"\'{p_name}\'":<25}", end="")

                        # Newline if last item
                        if i == len(format_parts) - 1:
                            print()

                    else:
                        # Write to right column
                        if i + 1 in added:
                            print(f"{col(f"{options[i]}) \'{p_name}\'", "red")}")

                        else:
                            print(f"{col(options[i], "cyan")}) \'{p_name}\'")

                # Display menu nav options
                print(f"\n  {col('S', 'cyan')}) Save")
                print(f"  {col('R', 'cyan')}) Reset")

                print(f"\n  Current Format: "
                      f"{col("None" if not cur_format else f"\'{cur_format}\'", "cyan")}")

                # Display message if any
                if msg:
                    print(f"{msg}")
                else:
                    print()

                print(f"{INFO} Enter the format number to add it to the filename.")

            @staticmethod
            def fc_adv_prompt() -> None:
                """
                Menu for entering yt-dlp filename format
                """
                print(
                    f"\n{col('●', "red")} Advanced Mode allows you to enter your own custom format [Also called Output Templates].")
                print(
                    f"{col('●', "magenta")} Make sure you enter a valid output template otherwise the value will be NA.")
                print(f"{col('●', "yellow")} More info on output templates: "
                      f"{col("\'https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template\'", "cyan")}")

                print(f"\n{INFO} Enter the filename format.")

        class Messages:
            """
            Messages for FC
            """

            @staticmethod
            def fc_simple_msg_reset() -> str:
                """
                Message to display when the filename format is reset
                :return: Message
                """
                return f"\n{SUCCESS} {col("Current Format has been reset.", "green")}"

            @staticmethod
            def fc_simple_msg_empty_format() -> str:
                """
                Error message when trying to use an empty filename format outside of edit mode
                :return Error
                """
                return f"\n{FAIL} {col("Filename format cannot be empty.", "red")}"

            @staticmethod
            def fc_simple_msg_part_added() -> str:
                """
                Error message when trying to add an already added part
                :return: Error
                """
                return f"\n{FAIL} {col("Part is already added. Reset to change parts.", "red")}"

    class Download:
        """
        Contains all menus/messages related to downloads
        """

        @staticmethod
        def processing_download():
            """
            Message to display while processing the URL
            """

            print(f"\n{ACTION} Preparing to download. Please wait...")

        @staticmethod
        def starting_download(count: int) -> None:
            """
            Message to display when the download starts
            :param count: Number of items to download
            """
            print(f"\n{ACTION} Starting to download {col(count, "yellow")} {"items" if count > 1 else "item"}. "
                  f"Please be patient as this might take a while...\n")

        @staticmethod
        def download_status(cur_item: int, total_items: int, downloaded: int, total: int, dwn_percent: float,
                            status: int,
                            title: str) -> None:
            """
            Download status message
            :param cur_item: Current item out of the total number of items to download
            :param total_items: Total number of items to download
            :param downloaded: Downloaded bytes
            :param total: Total bytes
            :param dwn_percent: Download percentage
            :param status: Status integer of download, from progress_hook
            :param title: Title of the item being downloaded

            Status codes:
                - ``0`` = Finished
                - ``1`` = Downloading
                - ``2`` = Post-Processing
                - ``-1`` = Error
            """

            # Convert sizes
            c_downloaded: str = Utilities.convert_bytes(downloaded)
            c_total: str = Utilities.convert_bytes(total)

            # Remove previous line
            print("", end="\x1b[1K\r")

            # Set status symbol
            if status == 1:
                sym_status: str = col("⧗", "cyan")
            elif status == 0:
                sym_status: str = col("✔", "green")
            elif status == -1:
                sym_status: str = col("✘", "red")
            elif status == 2:
                sym_status: str = col("⧗", "magenta")
            else:
                sym_status: str = col("?", "yellow")

            print(
                f"{col(f"({cur_item}/{total_items})", "yellow")} [{sym_status}] "
                f"{col(f"\'{title}\'", "cyan")}: {c_downloaded} / {c_total} "
                f"{col(f"({dwn_percent}%)", "magenta")}", end="")

        @staticmethod
        def download_status_a(cur_item: int, total_items: int, title: str) -> None:
            """
            Download status for Artwork downloads. Since yt-dlp skips download, there is no progress_hook. This is
            simply a workaround to display the progress. Only display cur/total items, and title
            :param cur_item: Current item
            :param total_items: Total items
            :param title: Title of item
            """
            print(f"{col(f"({cur_item}/{total_items})", "yellow")} [{col("✔", "green")}] "
                  f"{col(f"\'{title}\'", "cyan")}")

        @staticmethod
        def all_downloads_complete(completed: int, total: int, path_dir: str, size: str = "") -> None:
            """
            Message to display when all downloads are complete
            :param completed: Number of completed downloads
            :param total: Total number of downloads
            :param path_dir: Path to the directory where the downloads are saved
            :param size: Size string containing size of download and unit (bytes). If blank, will not display
            """
            print(f"\n\n\n{col('●', "red")}{col('●', "magenta")}{col('●', "yellow")}"
                  f" {col("Download Summary", "green", attrs=["bold", "underline"])} "
                  f"{col('●', "yellow")}{col('●', "magenta")}{col('●', "red")}")
            print(f"{SUCCESS} {col(completed, "yellow")} out of {col(total, "yellow")} item(s) downloaded "
                  f"successfully to {col(f"\'{path_dir}\'", "cyan")}.")

            if size:
                print(f"  Used {col(size, "yellow")} of storage.")

        @staticmethod
        def failed_downloads_list(failed: int, items: list[str]) -> None:
            """
            Displays all failed downloads in a list. Comes after `Menu.Main.all_downloads_complete`
            :param failed: Number of failed downloads
            :param items: List of failed downloads' titles
            """
            print(f"{FAIL} {col(failed, "red")} item(s) failed to download:")

            for title in items:
                print(f"  - {col(f"\'{title}\'", "cyan")}")

        @staticmethod
        def redownloading_item(item: str) -> None:
            """
            Message to display when the user wants to re-download an item
            :param item: Name of the item
            """
            print(f"{ACTION} Deleting {col(f"\'{item}\'", "cyan")} and re-downloading...")

    class Video:
        """
        Contains all menus for video downloads
        """

        @staticmethod
        def video_menu() -> None:
            """
            Displays list of video file formats
            """
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {col('1', "cyan")}) MP4")
            print(f"  {col('2', "cyan")}) MKV")
            print(f"  {col('3', "cyan")}) WEBM")

        @staticmethod
        def video_quality_status() -> None:
            """
            Status message to display while gathering video qualities from URL
            """
            print(f"\n{ACTION} Gathering video qualities. Please wait...", end="")

        @staticmethod
        def video_quality(qualities: list[str]) -> None:
            """
            Displays list of video qualities
            """

            # Get options
            options: list[str] = Utilities.menu_get_options(entries=len(qualities))

            print(f"\n{INFO} What video quality do you want to use?")

            for i, quality in enumerate(qualities):
                print(f"  {col(options[i], 'cyan')}) {quality}")

        @staticmethod
        def default_quality(quality: str) -> None:
            """
            Message to display when using default quality
            :param quality: Quality
            """
            print("", end="\x1b[1K\r")
            print(f"{INFO} Using default quality: {col(quality, 'cyan')}")

    class Audio:
        """
        Contains all menus for audio downloads
        """

        @staticmethod
        def audio_menu() -> None:
            """
            Displays list of audio file formats
            """
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {col('1', "cyan")}) MP3")
            print(f"  {col('2', "cyan")}) OGG")
            print(f"  {col('3', "cyan")}) WAV")
            print(f"  {col('4', "cyan")}) FLAC")

    class Artwork:
        """
        Contains all menus for artwork/thumbnail downloads
        """

        @staticmethod
        def artwork_menu() -> None:
            """
            Displays list of image file formats
            """
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {col('1', "cyan")}) PNG")
            print(f"  {col('2', "cyan")}) JPG")

    class Problem:
        """
        Any problems the script may encounter, such as duplicate files, bad URLs, or errors
        """

        class Success:
            """
            Messages to display when a problem is resolved
            """

            @staticmethod
            def duplicate_playlist(path: str) -> None:
                """
                Message to display when a playlist already exists on the user's device and user
                does not want to re-download
                :param path: Direct path to the playlist on the disk
                """
                print(f"\n{SUCCESS} Playlist is already downloaded to {col(f"\'{path}\'", "cyan")}.")

            @staticmethod
            def duplicate_single_item(path: str) -> None:
                """
                Message to display when a single item already exists on the user's
                device and user does not want to re-download
                :param path: Direct path to the item on the disk
                """
                print(f"\n{SUCCESS} Item is already downloaded to {col(f"\'{path}\'", "cyan")}.")

            @staticmethod
            def mode_change_single() -> None:
                """
                Message to display when user chooses to switch from Playlist to Single Item
                """
                print(f"\n{SUCCESS} Mode changed successfully from {col("Playlist", "red")} "
                      f"to {col("Single Item", "green")}. Continuing with download...")

            @staticmethod
            def mode_change_playlist() -> None:
                """
                Message to display when user chooses to switch from Single Item to Playlist
                """
                print(f"\n{SUCCESS} Mode changed successfully from {col("Single Item", "red")} "
                      f"to {col("Playlist", "green")}. Continuing with download...")

            @staticmethod
            def video_qualities_found(num_qualities: int) -> None:
                """
                Message to display when video qualities are found
                :param num_qualities: Number of video qualities found
                """
                print("", end="\x1b[1K\r")
                print(
                    f"{SUCCESS} Found {col(num_qualities, "cyan")} available video "
                    f"qualit{"ies" if num_qualities > 1 else "y"}.")

            @staticmethod
            def config_no_problems() -> None:
                """
                Message to display when the config file has no problems
                """
                print(f"\n{SUCCESS} {col("No problems found in the config file.", "green")}")

            @staticmethod
            def fc_default_changed() -> None:
                """
                Message to display when the default file format has changed
                """
                print(f"\n{SUCCESS} {col("Default file format changed successfully.", "green")}")

            @staticmethod
            def fc_cleared_defaults() -> None:
                """
                Message to display when all default filename formats have been cleared
                """
                print(f"\n{SUCCESS} {col("Default file formats have been cleared.", "green")}")

        class Warning:
            """
            Any problems that don't immediately cause an error, but require attention
            """

            @staticmethod
            def url_is_playlist() -> None:
                """
                Warning to display when the URL is a playlist, but "Single Item" was selected
                """
                print(f"\n{WARN} The URL contains more than one item, when "
                      f"{col("Single Item", "red")} mode was chosen.")
                print(f"\n{INFO} Do you want to switch to {col("Playlist", "green")} mode?")

            @staticmethod
            def url_is_single_item() -> None:
                """
                Warning to display when the URL is a single item, but "Playlist" was selected
                """
                print(f"\n{WARN} The URL contains only one item, when {col("Playlist", "red")} mode "
                      f"was chosen.\nDo you want to switch to {col("Single Item", "green")} mode?")

            @staticmethod
            def duplicate_playlist(title: str) -> None:
                """
                Warning when a playlist already exists on the user's device
                """
                print(f"\n{WARN} {col("The playlist", "yellow")} {col(f"\'{title}\'", "cyan")} "
                      f"{col("already exists. Do you want to re-download it?", "yellow")}")

            @staticmethod
            def duplicate_single_item(title: str) -> None:
                """
                Warning when a single item already exists on the user's device
                """
                print(f"\n{WARN} {col("The item", "yellow")} {col(f"\'{title}\'", "cyan")} "
                      f"{col("already exists. Do you want to re-download it?", "yellow")}")

            @staticmethod
            def no_video_qualities() -> None:
                """
                Message to display when no video qualities are found
                """
                print("", end="\x1b[1K\r")
                print(f"{WARN} {col("No available video qualities found. "
                                    "Using best quality.", "yellow")}")

            @staticmethod
            def default_quality_unavailable(quality: str, next_quality: str) -> None:
                """
                Warning to display when the default quality is unavailable
                :param quality: Quality
                :param next_quality: Next available quality
                """
                print("", end="\x1b[1K\r")
                print(
                    f"{WARN} {col(f"Default quality {quality} is not available. "
                                  f"Using next best quality: {next_quality}", "yellow")}")

            @staticmethod
            def config_problems(e: Exception | list[Exception]) -> None:
                """
                Warning to display when there is one or more problems with the config file that
                prevents the Downloader from working
                :param e: Config Error or list of Config Errors
                """

                num_errors: int = len(e) if isinstance(e, list) else 1
                print(f"\n{WARN} {col(f"Found {num_errors} problem{'s' if num_errors > 1 else ''} "
                                      f"with the configuration file:", "yellow")}")

                if isinstance(e, list):
                    for error in e:
                        print(col(f"  - {error}", "yellow"))

                else:
                    print(col(f"  - {e}", "yellow"))

            @staticmethod
            def config_force_reset() -> None:
                """
                Warning to display when the config file has to be reset due to being malformed
                """
                print(f"\n{WARN} {col("Config file is malformed and must be reset to default.", "yellow")}")

        class Error:
            """
            Any errors the script may encounter
            """

            @staticmethod
            def error_msg(error: Exception) -> None:
                """
                Generic error message
                :param error: Exception
                """
                print(f"\n{FAIL} {col(error, "red")}")

            @staticmethod
            def error_msg_crash(error: Exception) -> None:
                """
                Generic error message but with extra info
                :param error: Exception
                """
                print(f"\n{FAIL} {col(f"An error occurred: {error}", "red")}")
                print(col("  If you used an advanced filename format, make sure you enter it in correctly.", "red"))

            @staticmethod
            def dwn_size_error(error: Exception) -> None:
                """
                Generic error message when getting download size
                :param error: Exception
                """
                print(f"\n{FAIL} {col("An error occurred while trying to get the download size:", "red")}")
                print(col(f"  - {error}", "red"))

            @staticmethod
            def invalid_url() -> None:
                """
                Error when the URL is not valid
                """
                print(f"\n{FAIL} {col("Invalid URL. URL should start with 'https' or 'http'.", "red")}")

            @staticmethod
            def not_youtube_url(allowed_urls: list[str]) -> None:
                """
                Error when the URL is not a YouTube URL
                :param allowed_urls: List of allowed URLs
                """
                print(f"\n{FAIL} {col(f"Not a valid YouTube URL: '{"', '".join(allowed_urls)}'", "red")}")

            @staticmethod
            def incorrect_mode_single() -> None:
                """
                Error when user chooses the Playlist instead of Single Item, and does not want to switch
                """
                print(
                    f"\n{FAIL} Cannot download items due to incorrect mode selected. "
                    f"Please choose the right mode for the provided URL.")
                print(f"- Chosen Mode: {col("Playlist", "red")}")
                print(f"- Correct Mode: {col("Single Item", "green")}")

            @staticmethod
            def incorrect_mode_playlist() -> None:
                """
                Error when user chooses the Single Item instead of Playlist, and does not want to switch
                """
                print(
                    f"\n{FAIL} Cannot download items due to incorrect mode selected. "
                    f"Please choose the right mode for the provided URL.")
                print(f"- Chosen Mode: {col("Single Item", "red")}")
                print(f"- Correct Mode: {col("Playlist", "green")}")

            @staticmethod
            def pref_already_default() -> None:
                """
                Error when all preferences are already set to default
                """
                print(f"\n{FAIL} {col("Preferences are already set to default.", "red")}")

            @staticmethod
            def config_menu_error():
                """
                Error to display when a menu in Config Editor cannot be opened
                """
                print(f"\n{FAIL} {col("An error occurred that prevents opening this menu. "
                                      "Config reset may be required.", "red")}")

            @staticmethod
            def config_error(e: Exception | list[Exception], config_path: str) -> None:
                """
                Error when there is an issue with the config file
                :param e: Config Error or list of Config Errors
                :param config_path: Config Path
                """
                num_errors: int = len(e) if isinstance(e, list) else 1
                print(f"\n{FAIL} {col(f"Cannot run Downloader. The following "
                                      f"{f"{num_errors} " if num_errors > 1 else ''}"
                                      f"error{'s' if num_errors > 1 else ''} occurred:", "red")}")

                # Handle lists of errors
                if isinstance(e, list):
                    for error in e:
                        print(col(f"  - {error}", "red"))

                else:
                    print(col(f"  - {e}", "red"))

                print(f"\n  {col("Correct this issue in the config file or through the Config Editor."
                                 f"\n  - Config path: \'{config_path}\'"
                                 "\n  - Config Editor: \'main.py -c\' or \'main.py --config\'", "red")}")
