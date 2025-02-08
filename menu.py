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
        def exit_script():
            """
            Message when exiting the script, such as using CTRL+C
            """
            print(f"\n{ACTION} Exiting script...")

    class Input:
        """
        Contains all input prompts and input validation
        """

        @staticmethod
        def get_input_num(num_entries: int = 3, default_option: int = 1) -> int:
            """
            Gets a numeric input from the user
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
        def filename_format() -> None:
            """
            Get the format for the filename (uploader and title or just title)
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

        class Error:
            """
            Any errors the script may encounter
            """

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
