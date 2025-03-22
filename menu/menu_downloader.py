from utility.utils_menu import MenuUtilities
from utility.utils_misc import MiscUtilities
from .menu_colors import *
from .menu_misc import ArgumentMenu


class DwnMenu:
    """
    Menus for the Downloader
    """

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
                ArgumentMenu.show_version(v=v)

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
        def confirmation_screen(dwn_type: int, file_format: int, item_count: int,
                                pn_format: list[str] or None, pn_mode: int or None,
                                ff_mode: int, fn_format: list[str], video_quality: str or None) -> None:
            """
            Display a confirmation screen with all chosen options
            :param dwn_type: Download type
            :param file_format: File format
            :param item_count: Item count (Single Item/Playlist)
            :param pn_mode: Type of Playlist name format
            :param pn_format: Playlist name format
            :param ff_mode: Type of filename format
            :param fn_format: Filename format list
            :param video_quality: Video quality
            """

            # Get names of download choices
            v_dwn_type: str = MenuUtilities.get_download_type(dwn_type=dwn_type)
            v_file_format: str = MenuUtilities.get_file_format(file_format=file_format, dwn_type=dwn_type)
            v_item_count: str = MenuUtilities.get_download_mode(item_count=item_count)

            if pn_format[0]:
                v_playlist_format: str = MenuUtilities.get_playlist_name_format(pn_mode=pn_mode, pn_format=pn_format)
            else:
                v_playlist_format = ""

            v_filename_format: str = MenuUtilities.get_filename_format(item_count=item_count, ff_mode=ff_mode,
                                                                       filename_format=fn_format)

            # Display confirmation screen
            print(f"\n{INFO} Chosen Options:"
                  f"\n - Download Type: {col(f"'{v_dwn_type}'", "cyan")}"
                  f"\n - File Format: {col(f"'{v_file_format}'", "cyan")}"
                  f"\n - Mode: {col(f"'{v_item_count}'", "cyan")}", end="")

            # Hide Playlist name format for Single Item
            print(f"\n - Playlist Name Format: {col(f"'{v_playlist_format}'", "cyan")}" \
                      if pn_format[0] else "", end="")

            # Hide filename format for Artwork
            print(f"\n - Filename Format: {col(f"'{v_filename_format}'", "cyan")}" \
                      if dwn_type != 3 else "", end="")

            # Show video quality for Videos
            print(f"\n - Video Quality: {col(f"'{video_quality}'", "cyan")}" \
                      if video_quality else "", end="")

            print("\n")
            print(f"{INFO} Proceed with the download?")

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
            c_downloaded: str = MiscUtilities.convert_bytes(downloaded)
            c_total: str = MiscUtilities.convert_bytes(total)

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
            options: list[str] = MenuUtilities.menu_get_options(entries=len(qualities))

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
