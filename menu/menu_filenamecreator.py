from utility.utils_menu import MenuUtilities
from .menu_colors import *


class PlaylistNameMenu:
    """
    Special menus/messages for Playlist Name Creator
    """

    @staticmethod
    def format_mode() -> None:
        """
        Menu to choose which mode to use: Presets or Custom
        """
        print(f"\n{INFO} What type of playlist name format do you want to use?")
        print(f"  {col('1', "cyan")}) Presets")
        print(f"  {col('2', "cyan")}) Custom")

    @staticmethod
    def default_format(default_format: str) -> None:
        """
        Message to display in Downloader when using a default format
        :param default_format: Default filename format
        """
        print(f"\n{INFO} Using default playlist name format: {col(f"\'{default_format}\'", "cyan")}")

    @staticmethod
    def display_pn_full(pn_pref: list[str], item_num: int = 0) -> None:
        """
        Display full playlist name format tree. Used for Config Editor
        :param pn_pref: Default playlist name format preference
        :param item_num: Item number in Edit Config to display as #). Uses - if 0
        """

        # Item num display
        print(f"  {col(item_num, "cyan")}) " if item_num != 0 else "  - ", end="")

        # Display edit message if item num is set
        print(f"Default Playlist Name Format: "
              f"{col("Edit with Playlist Name Creator", "cyan") if item_num != 0 else ''}")

        print(f"      Display Format:  {col(f"\'{pn_pref[0]}\'", "magenta")}")
        print(f"      f-string Format: {col(f"\'{pn_pref[1]}\'", "magenta")}")
        print(f"      yt-dlp Format:   {col(f"\'{pn_pref[2]}\'", "magenta")}")

        if item_num == 0:
            print()

    class Presets:
        """
        Playlist Name format preset menus/messages
        """

        @staticmethod
        def preset_menu(presets: list[str]) -> None:
            """
            Get the format for the playlist name
            :param presets: List of presets
            """
            print(f"\n{INFO} What format do you want the playlist name to be?")

            for i, p in enumerate(presets):
                print(f"  {col(str(i + 1), 'cyan')}) {p}")

    class Custom:
        """
        Playlist Name format custom menus/messages
        """

        @staticmethod
        def pc_make_default(cur_format: str, default_format: str = "") -> None:
            """
            Prompt for setting default if it doesn't exist
            :param cur_format: Current format
            :param default_format: Default format saved if provided
            """
            if not default_format:
                print(f"\n{INFO} No default is set in the config for {col("Playlist Name", "cyan")}.")

            else:
                print(f"\n{INFO} Current default is {col(f"\'{default_format}\'", "cyan")}.")

            # If current format is empty and default is set, prompt for clearing default
            if not cur_format and default_format:
                print("  Do you want to remove the default format?")

            else:
                print(f"  Do you want to set it to {col(f"\'{cur_format}\'", "cyan")}?")


class FilenameMenu:
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
        def fc_header(edit_format: int, default_format: str = "", edit_format_s: str = "",
                      fc_title: str = "") -> None:
            """
            Display header for Filename Creator
            :param edit_format: Default format to edit
            :param default_format: Default filename format if it exists
            :param edit_format_s: Default format being edited. Required if edit default is not 1 or 2
            :param fc_title: Title of Filename Creator. Optional
            """
            print(f"\n{col('●', "red")} Welcome to the {col(
                fc_title if fc_title else "Filename Creator", "red")}!")

            print(f"{col('●', "magenta")} Construct your own format names for your downloads.")

            print(f"{col('●', "yellow")} Editing Format: ", end="")

            match edit_format:
                case 1:
                    print(f"{col("Single Item", "cyan")}")
                case 2:
                    print(f"{col("Playlist", "cyan")}")
                case _:
                    print(f"{col(edit_format_s, "cyan")}")

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
        def fc_def_format(edit_format: int, defaults: list[str]) -> None:
            """
            Menu to get which default format to edit for when using FC through argument
            :param edit_format: Default format to edit
            :param defaults: List of default formats for each download mode
            """

            # Custom header for edit mode
            print(f"\n{col('●', "red")} {col("[EDIT MODE]", "yellow")}: "
                  "Edit each default format individually.")
            print(f"\n{col('●', "magenta")} Current Defaults:")

            # Filename Formats
            print(f"{col('●', "yellow")} Single Item: {col(
                "None" if not defaults[0] else f"\'{defaults[0]}\'", "cyan")}")

            print(f"{col('●', "yellow")} Playlist: {col(
                "None" if not defaults[1] else f"\'{defaults[1]}\'", "cyan")}")

            # Playlist Name Format
            print(f"{col('●', "yellow")} Playlist Name: {col(
                "None" if not defaults[2] else f"\'{defaults[2]}\'", "cyan")}")

            print(f"\n{INFO} What default format do you want to edit?")
            print(f"  {col('1', 'cyan')}) Single Item")
            print(f"  {col('2', 'cyan')}) Playlist")
            print(f"  {col('3', 'cyan')}) Playlist Name")
            print(f"  {col('4', 'cyan')}) Clear Defaults")

            # Don't show launch downloader if coming from Config Editor
            if edit_format != -1:
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
            options: list[str] = MenuUtilities.menu_get_options(entries=len(format_parts))

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
