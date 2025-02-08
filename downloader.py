import yt_dlp as yt
from threading import Thread
from pathlib import Path


class Downloader:
    """
    Handles the downloading of videos, audio, and thumbnails
    Basically, all the yt-dlp functionality
    """

    # Silence yt-dlp output
    class QuietLogger:

        # Silence debug output
        def debug(self, msg): pass

        # Silence warnings
        def warning(self, msg): pass

        # Silence errors
        def error(self, msg): pass

    @staticmethod
    def get_title_count(url: str) -> int:
        titles: list[str] = []

        ydl_args = {
            "logger": Downloader.QuietLogger(),
            "extract_flat": True,
            "force_generic_extractor": False,
            "quiet": True,
        }

        # Extract all the titles from the URL
        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                result = ydl.extract_info(url, download=False)

                # Handle playlists
                if "entries" in result:
                    titles = [entry.get("title", "") for entry in result["entries"]]
                else:
                    titles = [result.get("title", "")]

            except Exception as e:
                print(f"Error: {e}")

        return len(titles)

    @staticmethod
    def get_download_size(path: str, unit: str) -> str:
        """
        Get the size of the downloaded file or directory
        :param path: Direct path to a file or directory
        :param unit: Unit name: "KB", "MB", "GB", "Auto"
        :return: String containing the size and unit (bytes)
        """

        size_b: int = 0

        # Check if path is a file or directory
        if Path(path).is_dir():

            # Iterate through all files in the directory and calculate the size
            for file in Path(path).iterdir():
                size_b += file.stat().st_size

        else:
            # Get size of single file
            size_b = Path(path).stat().st_size

        # Convert bytes to desired unit
        if unit.upper() == "KB" or unit.upper() == "K":
            # Kilobytes
            size: float = size_b / 1024
            return f"{size:.2f} KB"

        elif unit.upper() == "MB" or unit.upper() == "M":
            # Megabytes
            size: float = size_b / (1024 * 1024)
            return f"{size:.2f} MB"

        elif unit.upper() == "GB" or unit.upper() == "G":
            # Gigabytes
            size: float = size_b / (1024 * 1024 * 1024)
            return f"{size:.2f} GB"

        elif unit.upper() == "AUTO":
            # Auto: Determine unit automatically
            if size_b < 1024:
                # Less than 1 KB
                size: float = size_b
                return f"{size:.2f} B"

            elif size_b < (1024 ** 2):
                # Less than 1 MB
                size: float = size_b / 1024
                return f"{size:.2f} KB"

            elif size_b < (1024 ** 3):
                # Less than 1 GB
                size: float = size_b / (1024 ** 2)
                return f"{size:.2f} MB"

            else:
                # Greater than 1 GB
                size: float = size_b / (1024 ** 3)
                return f"{size:.2f} GB"

        else:
            return ""

    @staticmethod
    def get_playlist_name(url: str) -> str:

        ydl_args = {
            "logger": Downloader.QuietLogger(),
            "extract_flat": True,
            "force_generic_extractor": False,
            "quiet": True,
        }

        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                playlist = ydl.extract_info(url, download=False)
                return str(playlist["title"])

            except Exception as e:
                print(f"Error: {e}")
                return ""

    @staticmethod
    def setup_ytdlp_options(dwn_type: int, file_format: int, item_count: int,
                            dwn_dir: str, filename_format: int, playlist_name: str) -> dict:
        """
        Sets up the yt-dlp options
        :param dwn_type: Download type: 1 = Video, 2 = Audio, 3 = Artwork
        :param file_format: File format: Depends on download type
        :param item_count: Number of items: 1 = Single item, 2 = Playlist
        :param dwn_dir: Download directory
        :param filename_format: Filename format: 1 = (uploader) - (title).(ext), 2 = (title).(ext)
        :param playlist_name: Playlist name
        :return: dictionary containing all yt-dlp options
        """

        # Setup yt-dlp options
        ytdlp_options: dict = {
            "logger": Downloader.QuietLogger(),
            "quiet": True
        }

        # -------------------------------------------------------------------------------
        #                               Setup Format
        # -------------------------------------------------------------------------------

        # File formats based on download type
        if dwn_type == 1:

            # Video
            if file_format == 1:
                ytdlp_options["format"] = "bestvideo+bestaudio"
                ytdlp_options["merge_output_format"] = "mp4"

            elif file_format == 2:
                ytdlp_options["format"] = "bestvideo+bestaudio"
                ytdlp_options["merge_output_format"] = "mkv"

            elif file_format == 3:
                ytdlp_options["format"] = "bestvideo+bestaudio"
                ytdlp_options["merge_output_format"] = "webm"

        elif dwn_type == 2:

            # Audio
            if file_format == 1:
                ytdlp_options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }]

            elif file_format == 2:
                ytdlp_options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "vorbis",
                    "preferredquality": "0",
                }]

            elif file_format == 3:
                ytdlp_options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "0",
                }]

            elif file_format == 4:
                ytdlp_options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "flac",
                    "preferredquality": "0",
                }]

        elif dwn_type == 3:

            # Artwork
            ytdlp_options["skip_download"] = True
            ytdlp_options["writethumbnail"] = True

        # -------------------------------------------------------------------------------
        #                               Setup Path
        # -------------------------------------------------------------------------------

        # Single item
        if item_count == 1:

            # (uploader) - (title).(ext)
            if filename_format == 1 and dwn_type != 3:
                ytdlp_options["outtmpl"] = f"{dwn_dir}%(uploader)s - %(title)s.%(ext)s"

            # (title).(ext)
            elif filename_format == 2:
                ytdlp_options["outtmpl"] = f"{dwn_dir}%(title)s.%(ext)s"

        # Playlist
        elif item_count == 2:

            # (uploader) - (title).(ext)
            if filename_format == 1 and dwn_type != 3:
                ytdlp_options["outtmpl"] = f"{dwn_dir}{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

            # (title).(ext)
            elif filename_format == 2:
                ytdlp_options["outtmpl"] = f"{dwn_dir}{playlist_name}/%(title)s.%(ext)s"

        return ytdlp_options

    @staticmethod
    def extract_info(item_count: int, yt_url: str) -> tuple[list[str], list[str], list[str]]:
        """
        Extract all info from a YouTube url
        :param item_count: Number of items: 1 = Single item, 2 = Playlist
        :param yt_url: YouTube URL
        :return: Returns a tuple of (titles, uploaders, urls)
        """

        titles: list[str] = []
        uploaders: list[str] = []
        urls: list[str] = []

        # Setup yt-dlp args
        ydl_args = {
            "logger": Downloader.QuietLogger(),
            "extract_flat": True,
            "force_generic_extractor": False,
            "quiet": True,
        }

        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                result = ydl.extract_info(yt_url, download=False)

                # Handle playlists
                if "entries" in result:
                    entries = result["entries"]
                else:
                    entries = [result]

                # Loop through the entries and extract info
                for entry in entries:
                    titles.append(entry.get("title", "Unknown"))
                    uploaders.append(entry.get("uploader", "Unknown"))

                    # Only collect urls if it's a playlist
                    if item_count == 2:
                        urls.append(entry.get("url", "Unknown"))

            except Exception as e:
                print(f"Error: {e}")

        return titles, uploaders, urls

    @staticmethod
    def download(url: str, ytdlp_options: dict) -> bool:
        """
        Download an item
        :param url: YouTube URL
        :param ytdlp_options: Dictionary of yt-dlp options
        """

        def download_thread():
            with yt.YoutubeDL(ytdlp_options) as ydl:
                ydl.download([url])

        try:
            thread: Thread = Thread(target=download_thread)
            thread.start()

            # Wait for the download to finish
            thread.join()

            return True

        except (yt.DownloadError, yt.DownloadCancelled) as _:
            return False
