from .menu_colors import *


class ConfigProblem:
    """
    Config Editor problems
    """

    class Success:
        """
        Messages to display when a problem is resolved
        """

        @staticmethod
        def config_no_problems() -> None:
            """
            Message to display when the config file has no problems
            """
            print(f"\n{SUCCESS} {col("No problems found in the config file.", "green")}")

    class Warning:
        """
        Any problems that don't immediately cause an error, but require attention
        """

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


class FilenameProblem:
    """
    Filename Creator problems
    """

    class Success:
        """
        Messages to display when a problem is resolved
        """

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
        pass

    class Error:
        """
        Any errors the script may encounter
        """
        pass


class DwnProblem:
    """
    Downloader problems
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

    class Warning:
        """
        Any problems that don't immediately cause an error, but require attention
        """

        @staticmethod
        def download_aborted() -> None:
            """
            Message when a download is aborted (Choosing N on the confirmation menu)
            """
            print(f"\n{WARN} {col("Download aborted.", "yellow")}")

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

    class Error:
        """
        Any errors the script may encounter
        """

        @staticmethod
        def dwn_size_error(error: Exception) -> None:
            """
            Generic error message when getting download size
            :param error: Exception
            """
            print(f"\n{FAIL} {col("An error occurred while trying to get the download size:", "red")}")
            print(col(f"  - {error}", "red"))

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


class InputProblem:
    """
    Input problems
    """

    class Success:
        """
        Messages to display when a problem is resolved
        """
        pass

    class Warning:
        """
        Any problems that don't immediately cause an error, but require attention
        """
        pass

    class Error:
        """
        Any errors the script may encounter
        """

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


class MiscProblem:
    """
    Miscellaneous problems, such as generic messages
    """

    class Success:
        """
        Messages to display when a problem is resolved
        """
        pass

    class Warning:
        """
        Any problems that don't immediately cause an error, but require attention
        """
        pass

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
