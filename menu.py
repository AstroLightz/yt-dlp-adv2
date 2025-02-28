from termcolor import colored

# Message types
SUCCESS: str = f"{colored('✔', "green")}"
FAIL: str = f"{colored('✘', "red")}"
INFO: str = f"{colored('?', "yellow")}"
WARN: str = f"{colored('⚠️', "yellow")}"
ACTION: str = f"{colored('➜', "blue")}"

# ANSI Codes for input
CYAN: str = "\033[36m"
RESET: str = "\033[0m"


class Menu:
    """
    Contains all menus for the program
    """

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
            print(f"\n{WARN} {colored("Download aborted.", "yellow")}")

    class Input:
        """
        Contains all input prompts and input validation
        """

        @staticmethod
        def get_input_num(num_entries: int = 3, default_option: int = 1) -> int:
            """
            Gets a numeric input from the user. If num_entries is greater than 8, use `Menu.Input.get_input_long()` instead.
            :param default_option: The default option to select
            :param num_entries: Number of entries in the menu. Must be at least 2
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
                    choice: int = int(
                        input(
                            f"> {colored(options_list, "magenta")} {colored(f"({default_option})", "cyan")}: ") or default_option)

                    if choice < 1 or choice > num_entries:
                        raise ValueError

                    return choice

                except ValueError:
                    print(
                        f"\n{FAIL} {colored(f"Invalid input. Please enter an integer between 1 and {num_entries}.", "red")}")

        @staticmethod
        def get_input_long(num_entries: int = 3, default_option: int = 1) -> int:
            """
            Similar to get_input_num, but after 9 entries, the list goes to 0, then A, B, C, etc.
            :param default_option: The default option to select
            :param num_entries: Number of entries in the menu. Must be at least 2
            :return: The selected option
            """

            # Create options list string
            options_list: str = "["

            # Calculate the max entries string
            if num_entries > 10:
                # User chars
                max_entries_str: str = chr(54 + num_entries)

            elif num_entries > 9:
                # 10 entries: use 0
                max_entries_str: str = "0"

            else:
                # 1-9 entries: use the number
                max_entries_str = str(num_entries)

            for i in range(num_entries):
                if i != num_entries - 1:

                    # If the number is less than 10, add it to the list
                    if i < 9:
                        options_list += f"{i + 1}/"
                    # If the number is 10, add 0 to the list
                    elif i == 9:
                        options_list += "0/"

                    # If the number is greater than 10, add the letter to the list (A, B, C, etc.)
                    else:
                        options_list += f"{chr(55 + i)}/"

                else:

                    if i < 9:
                        options_list += f"{i + 1}"
                    elif i == 9:
                        options_list += "0"
                    else:
                        options_list += f"{chr(55 + i)}"

            options_list += "]"

            while True:
                try:
                    choice_str: str = (input(
                        f"> {colored(options_list, "magenta")} {colored(f"({default_option})", "cyan")}: ").upper()
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
                            f"\n{FAIL} {colored(f"Invalid input. Please enter an integer or letter between 1-0 and "
                                                f"{f"A-{max_entries_str}" if num_entries > 11 else max_entries_str}.", "red")}")

                    else:
                        print(
                            f"\n{FAIL} {colored(f"Invalid input. Please enter an integer between 1 and {"0" if num_entries > 9 else num_entries}.", "red")}")

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
                        f"> {colored(f"[{'Y' if default_option else 'y'}/{'N' if not default_option else 'n'}]", "magenta")}: "
                    ).lower()

                    if choice not in ["y", "n"] and choice != "":
                        raise ValueError
                    elif choice == "":
                        return default_option

                    # Returns true if choice is "y", false if choice is "n"
                    return choice == "y"

                except ValueError:
                    print(
                        f"\n{FAIL} {colored("Invalid input. Please enter 'Y' or 'N'.", "red")}")

        @staticmethod
        def get_input_url() -> str:
            """
            Get the URL of the item
            :return: The URL of the item
            """
            while True:
                try:
                    url: str = input(f"> {CYAN}")

                    # Reset ANSI codes
                    print(RESET, end="")

                    if ("https://" not in url and "http://" not in url) or url == "":
                        raise ValueError

                    return url

                except ValueError:
                    print(
                        f"\n{FAIL} {colored('Invalid input. Please enter a valid URL.', 'red')}")

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
        def program_header() -> None:
            """
            Header to be displayed when the script is launched
            """
            print(f"\nWelcome to {colored("YouTube Downloader: Advanced 2.0!", "red")}!\n")

            print(
                f"{colored('●', "red")} This is a Python program that simplifies the use of the "
                f"{colored("yt-dlp", "red")} tool ({colored("https://github.com/yt-dlp/yt-dlp", "cyan")}).")
            print(
                f"{colored('●', "red")} It provides a menu-driven interface to help you "
                f"download videos, audio, and thumbnails from YouTube.")
            print(
                f"{colored('●', "red")} You can customize download options and formats without "
                f"needing to remember complex yt-dlp arguments.")
            print(f"{colored('●', "red")} The program supports downloading entire playlists or single items.")
            print(f"{colored('●', "red")} It also offers detailed feedback on the download status and file sizes.\n")
            print(
                f"{colored('●', "magenta")} This is a remake of the original {colored('yt-dlp-adv', 'cyan')}, "
                f"now with new features and quality-of-life improvements.")
            print(f"{colored('●', "yellow")} Script made by {colored("AstroLightz", "cyan")}. I hope you enjoy!\n\n")

        @staticmethod
        def main_menu() -> None:
            """
            Displays list of download types
            """
            print(f"\n{INFO} What would you like to download?")
            print(f"  {colored('1', "cyan")}) Videos")
            print(f"  {colored('2', "cyan")}) Audio")
            print(f"  {colored('3', "cyan")}) Thumbnails")

        @staticmethod
        def item_count() -> None:
            """
            Get if item is a playlist or single item
            """
            print(f"\n{INFO} Is it a playlist or a single item?")
            print(f"  {colored('1', "cyan")}) Single Item")
            print(f"  {colored('2', "cyan")}) Playlist")

        @staticmethod
        def filename_format_s() -> None:
            """
            [Single Item] Get the format for the filename
            """
            print(f"\n{INFO} What format do you want the filenames to be?")
            print(f"  {colored('1', "cyan")}) (uploader) - (title).(ext)")
            print(f"  {colored('2', "cyan")}) (title).(ext)")

        @staticmethod
        def filename_format_p() -> None:
            """
            [Playlist] Get the format for the filename
            """
            print(f"\n{INFO} What format do you want the filenames to be?")
            print(f"  {colored('1', "cyan")}) (uploader) - (title).(ext)")
            print(f"  {colored('2', "cyan")}) (title).(ext)")

        @staticmethod
        def get_url() -> None:
            """
            Get the URL of the item
            """
            print(f"\n{INFO} Enter the YouTube URL:")

        @staticmethod
        def confirmation_screen(dwn_type: int, file_format: int, item_count: int, filename_format: int) -> None:
            """
            Display a confirmation screen with all chosen options
            :param dwn_type: Download type
            :param file_format: File format
            :param item_count: Item count (Single Item/Playlist)
            :param filename_format: Filename format
            """

            # Key/values for each option
            options: dict[str, dict[int, str]] = {
                "dwn_type": {
                    1: "Video",
                    2: "Audio",
                    3: "Artwork"
                },
                "file_format_vid": {
                    1: "MP4",
                    2: "MKV",
                    3: "WEBM"
                },
                "file_format_aud": {
                    1: "MP3",
                    2: "OGG",
                    3: "WAV",
                    4: "FLAC"
                },
                "file_format_art": {
                    1: "PNG",
                    2: "JPG"
                },
                "item_count": {
                    1: "Single Item",
                    2: "Playlist"
                },
                "filename_format_s": {
                    1: "(uploader) - (title).(ext)",
                    2: "(title).(ext)"
                },
                "filename_format_p": {
                    1: "(uploader) - (title).(ext)",
                    2: "(title).(ext)"
                }
            }

            # Get all values for each option
            v_dwn_type: str = options["dwn_type"][dwn_type]

            if dwn_type == 1:
                v_file_format: str = options["file_format_vid"][file_format]
            elif dwn_type == 2:
                v_file_format: str = options["file_format_aud"][file_format]
            else:
                v_file_format: str = options["file_format_art"][file_format]

            v_item_count: str = options["item_count"][item_count]

            if item_count == 1:
                v_filename_format: str = options["filename_format_s"][filename_format]
            else:
                v_filename_format: str = options["filename_format_p"][filename_format]

            # Display confirmation screen
            print(f"\n{INFO} Chosen Options:"
                  f"\n - Download Type: {colored(f"'{v_dwn_type}'", "cyan")}"
                  f"\n - File Format: {colored(f"'{v_file_format}'", "cyan")}"
                  f"\n - Mode: {colored(f"'{v_item_count}'", "cyan")}"
                  f"\n - Filename Format: {colored(f"'{v_filename_format}'", "cyan")}\n")

            print(f"{INFO} Proceed with the download?")

    class Download:
        """
        Contains all menus/messages related to downloads
        """

        @staticmethod
        def processing_url():
            """
            Message to display while processing the URL
            """

            print(f"\n{ACTION} Processing URL. Please wait...")

        @staticmethod
        def starting_download(count: int) -> None:
            """
            Message to display when the download starts
            :param count: Number of items to download
            """
            print(f"\n{ACTION} Starting to download {colored(count, "yellow")} {"items" if count > 1 else "item"}. "
                  f"Please be patient as this might take a while...\n")

        @staticmethod
        def download_status(cur_item: int, total_items: int, title: str) -> None:
            """
            Download status message
            :param cur_item: Current item out of the total number of items to download
            :param total_items: Total number of items to download
            :param title: Title of the item being downloaded
            """
            print(
                f"{colored(f"({cur_item}/{total_items})", "yellow")} Downloading: {colored(f"\'{title}\'", "cyan")} ... ",
                end="")

        @staticmethod
        def download_complete() -> None:
            """
            Appending string to be used at the end of `Menu.Main.downloading` if the download is successful
            """
            print(f"{colored("Completed", "green")}")

        @staticmethod
        def download_failed() -> None:
            """
            Appending string to be used at the end of `Menu.Main.downloading` if the download fails
            """
            print(f"{colored("Failed", "red")}")

        @staticmethod
        def all_downloads_complete(completed: int, total: int, path_dir: str, size: str) -> None:
            """
            Message to display when all downloads are complete
            :param completed: Number of completed downloads
            :param total: Total number of downloads
            :param path_dir: Path to the directory where the downloads are saved
            :param size: Size string containing size of download and unit (bytes)
            """
            print(f"\n\n\n{colored('●', "red")}{colored('●', "magenta")}{colored('●', "yellow")}"
                  f" {colored("Download Summary", "green", attrs=["bold", "underline"])} "
                  f"{colored('●', "yellow")}{colored('●', "magenta")}{colored('●', "red")}")
            print(f"{SUCCESS} {colored(completed, "yellow")} out of {colored(total, "yellow")} item(s) downloaded "
                  f"successfully to {colored(f"\'{path_dir}\'", "cyan")}. ")
            print(f"Used {colored(size, "yellow")} of storage.")

        @staticmethod
        def failed_downloads_list(failed: int, items: list[str]) -> None:
            """
            Displays all failed downloads in a list. Comes after `Menu.Main.all_downloads_complete`
            :param failed: Number of failed downloads
            :param items: List of failed downloads' titles
            """
            print(f"{FAIL} {colored(failed, "red")} item(s) failed to download:")

            for title in items:
                print(f"  - {colored(f"\'{title}\'", "cyan")}")

        @staticmethod
        def redownloading_item(item: str) -> None:
            """
            Message to display when the user wants to re-download an item
            :param item: Name of the item
            """
            print(f"{ACTION} Deleting {colored(f"\'{item}\'", "cyan")} and re-downloading...")

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
            print(f"  {colored('1', "cyan")}) MP4")
            print(f"  {colored('2', "cyan")}) MKV")
            print(f"  {colored('3', "cyan")}) WEBM")

        @staticmethod
        def video_quality_status() -> None:
            """
            Status message to display while gathering video qualities from URL
            """
            print(f"\n{ACTION} Gathering video qualities. Please wait...")

        @staticmethod
        def video_quality(qualities: list[str]) -> None:
            """
            Displays list of video qualities
            """
            print(f"\n{INFO} What video quality do you want to use?")

            for i, quality in enumerate(qualities):
                print(f"  {colored(str(i + 1), 'cyan')}) {quality}")

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
            print(f"  {colored('1', "cyan")}) MP3")
            print(f"  {colored('2', "cyan")}) OGG")
            print(f"  {colored('3', "cyan")}) WAV")
            print(f"  {colored('4', "cyan")}) FLAC")

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
            print(f"  {colored('1', "cyan")}) PNG")
            print(f"  {colored('2', "cyan")}) JPG")

    class Arguments:
        """
        Contains all menus for arguments passed to the script
        """

        @staticmethod
        def help_menu() -> None:
            """
            Displays help menu
            """
            print(f"{INFO} Usage: yt-dlp-adv2 {CYAN}[options]{RESET}"
                  f"\n\nOptions:"
                  f"\n{CYAN}-h, --help{RESET}: Show this help message."
                  f"\n{CYAN}-v, --version{RESET}: Show script version.")

        @staticmethod
        def show_version(v: str, g_commits: str) -> None:
            """
            Displays script version and GitHub link for commits/updates
            :param v: Version string
            :param g_commits: GitHub commits link
            """
            print(f"{INFO} Script version: {colored(v, 'cyan')}")
            print(f"{INFO} GitHub commits: {colored(g_commits, 'cyan')}")

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
                Message to display when a playlist already exists on the user's device and user does not want to re-download
                :param path: Direct path to the playlist on the disk
                """
                print(f"\n{SUCCESS} Playlist is already downloaded to {colored(path, "cyan")}.")

            @staticmethod
            def duplicate_single_item(path: str) -> None:
                """
                Message to display when a single item already exists on the user's device and user does not want to re-download
                :param path: Direct path to the item on the disk
                """
                print(f"\n{SUCCESS} Item is already downloaded to {colored(path, "cyan")}.")

            @staticmethod
            def mode_change_single() -> None:
                """
                Message to display when user chooses to switch from Playlist to Single Item
                """
                print(f"\n{SUCCESS} Mode changed successfully from {colored("Playlist", "red")} "
                      f"to {colored("Single Item", "green")}. Continuing with download...")

            @staticmethod
            def mode_change_playlist() -> None:
                """
                Message to display when user chooses to switch from Single Item to Playlist
                """
                print(f"\n{SUCCESS} Mode changed successfully from {colored("Single Item", "red")} "
                      f"to {colored("Playlist", "green")}. Continuing with download...")

        class Warning:
            """
            Any problems that don't immediately cause an error, but require attention
            """

            @staticmethod
            def url_is_playlist() -> None:
                """
                Warning to display when the URL is a playlist, but "Single Item" was selected
                """
                print(f"\n{WARN} The URL contains more than one item, when {colored("Single Item", "red")} mode "
                      f"was chosen.")
                print(f"\n{INFO} Do you want to switch to {colored("Playlist", "green")} mode?")

            @staticmethod
            def url_is_single_item() -> None:
                """
                Warning to display when the URL is a single item, but "Playlist" was selected
                """
                print(f"\n{WARN} The URL contains only one item, when {colored("Playlist", "red")} mode "
                      f"was chosen.\nDo you want to switch to {colored("Single Item", "green")} mode?")

            @staticmethod
            def duplicate_playlist(title: str) -> None:
                """
                Warning when a playlist already exists on the user's device
                """
                print(f"\n{WARN} The playlist {colored(f"\'{title}\'", "cyan")} already exists. "
                      f"Do you want to re-download it?")

            @staticmethod
            def duplicate_single_item(title: str) -> None:
                """
                Warning when a single item already exists on the user's device
                """
                print(f"\n{WARN} The item {colored(f"\'{title}\'", 'cyan')} already exists. "
                      f"Do you want to re-download it?")

            @staticmethod
            def no_video_qualities() -> None:
                """
                Message to display when no video qualities are found
                """
                print(f"\n{WARN} No video qualities found. Downloading with default quality.")

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
                print(f"{FAIL} {colored(error, "red")}")

            @staticmethod
            def invalid_url() -> None:
                print(f"{FAIL} The entered URL is not valid. Please make sure the URL starts with "
                      f"{colored("\'https\'", "cyan")} or {colored("\'http\'", "cyan")}.")

            @staticmethod
            def incorrect_mode_single() -> None:
                """
                Error when user chooses the Playlist instead of Single Item, and does not want to switch
                """
                print(
                    f"\n{FAIL} Cannot download items due to incorrect mode selected. Please choose the right mode for the provided URL.")
                print(f"- Chosen Mode: {colored("Playlist", "red")}")
                print(f"- Correct Mode: {colored("Single Item", "green")}")

            @staticmethod
            def incorrect_mode_playlist() -> None:
                """
                Error when user chooses the Single Item instead of Playlist, and does not want to switch
                """
                print(
                    f"\n{FAIL} Cannot download items due to incorrect mode selected. Please choose the right mode for the provided URL.")
                print(f"- Chosen Mode: {colored("Single Item", "red")}")
                print(f"- Correct Mode: {colored("Playlist", "green")}")
