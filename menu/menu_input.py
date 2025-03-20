from typing import Any

from utility.utils_downloader import DwnUtilities
from utility.utils_menu import MenuUtilities
from videoquality import VideoQuality
from .menu_colors import *
from .menu_problems import InputProblem


class Input:
    """
    Contains all input prompts and input validation
    """

    class String:
        """
        Input functions that return a string
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
                options_list, max_entries_str = MenuUtilities.input_get_options(entries=len(opt_range))

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
                    is_allowed = DwnUtilities.is_allowed_url(url=url, allowed_urls=allowed)

                    if not is_allowed:
                        raise ValueError

                    return url

                except ValueError:
                    if not is_allowed:
                        InputProblem.Error.not_youtube_url(allowed_urls=allowed)

                    else:
                        InputProblem.Error.invalid_url()

    class Integer:
        """
        Input functions that return an integer
        """

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
            options_list, max_entries_str = MenuUtilities.input_get_options(entries=num_entries)

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

    class Boolean:
        """
        Input functions that return a boolean
        """

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

    class Preference:
        """
        Input functions that returns something relating to preferences
        """

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
