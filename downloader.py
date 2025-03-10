from math import ceil
from pathlib import Path
from threading import Thread

import yt_dlp as yt

from videoquality import VideoQuality


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
                            dwn_dir: str, filename_format: int, playlist_name: str, video_quality: str) -> dict:
        """
        Sets up the yt-dlp options
        :param dwn_type: Download type: 1 = Video, 2 = Audio, 3 = Artwork
        :param file_format: File format: Depends on download type
        :param item_count: Number of items: 1 = Single item, 2 = Playlist
        :param dwn_dir: Download directory
        :param filename_format: Filename format: 1 = (uploader) - (title).(ext), 2 = (title).(ext)
        :param playlist_name: Playlist name
        :param video_quality: Video quality if specified
        :return: dictionary containing all yt-dlp options
        """

        # Qualities to yt-dlp format
        ytdlp_qualities: dict[str, str] = {

            "144p": "bestvideo[height=144]",
            "240p": "bestvideo[height=240]",
            "360p": "bestvideo[height=360]",
            "480p": "bestvideo[height=480]",
            "720p": "bestvideo[height=720][fps<60]",
            "720p60": "bestvideo[height=720][fps=60]",
            "1080p60": "bestvideo[height=1080][fps=60]",
            "2K": "bestvideo[height=1440]",
            "4K": "bestvideo[height=2160]",
            "2K60": "bestvideo[height=1440][fps=60]",
            "4K60": "bestvideo[height=2160][fps=60]"
        }

        # Setup yt-dlp options
        ytdlp_options: dict = {
            "logger": Downloader.QuietLogger(),
            "quiet": True,
            "restrictfilenames": True,
        }

        # -------------------------------------------------------------------------------
        #                               Setup Format
        # -------------------------------------------------------------------------------

        # File formats based on download type
        if dwn_type == 1:

            # Default to 'bestvideo+bestaudio' if video quality is not specified
            if not video_quality:
                ytdlp_format: str = "bestvideo+bestaudio"
            else:
                ytdlp_format: str = f"{ytdlp_qualities[video_quality]}+bestaudio"

            # Video
            if file_format == 1:
                ytdlp_options["format"] = ytdlp_format
                ytdlp_options["merge_output_format"] = "mp4"

            elif file_format == 2:
                ytdlp_options["format"] = ytdlp_format
                ytdlp_options["merge_output_format"] = "mkv"

            elif file_format == 3:
                ytdlp_options["format"] = ytdlp_format
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

            # (item #) - (uploader) - (title).(ext)
            elif filename_format == 3:
                ytdlp_options[
                    "outtmpl"] = f"{dwn_dir}{playlist_name}/%(playlist_index)s - %(uploader)s - %(title)s.%(ext)s"

            # (item #) - (title).(ext)
            elif filename_format == 4:
                ytdlp_options["outtmpl"] = f"{dwn_dir}{playlist_name}/%(playlist_index)s - %(title)s.%(ext)s"

        return ytdlp_options

    @staticmethod
    def extract_info(yt_url: str) -> tuple[list[str], list[str]]:
        """
        Extract all info from a YouTube URL
        :param yt_url: URL
        :return: Returns a tuple of (titles, uploaders)
        """

        titles: list[str] = []
        uploaders: list[str] = []

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


            except Exception as e:
                print(f"Error: {e}")

        return titles, uploaders

    @staticmethod
    def download(url: str, ytdlp_options: dict, dwn_type: int, item_count: int, filename_format: int,
                 titles: list[str], uploaders: list[str],
                 progress_callback=None) -> [int, int]:
        """
        Download an item
        :param url: YouTube URL
        :param ytdlp_options: Dictionary of yt-dlp options
        :param dwn_type: Download type
        :param item_count: Item count
        :param filename_format: Filename format
        :param titles: List of titles
        :param uploaders: List of uploaders
        :param progress_callback: Progress callback
        :return: Returns True if successful
        """

        dwn_status: int = 0
        cur_item: int = 1
        new_item: int = 0
        cur_process: int = 1

        # Saved downloaded/total when entering post-processing
        s_downloaded: int = 0
        s_total: int = 0

        post_processing: bool = False

        # Setup progress hook
        def progress_hook(data: dict):

            nonlocal dwn_status, cur_item, new_item, cur_process, post_processing, s_downloaded, s_total

            # Get status
            status: str = data.get("status")

            # Get title
            title: str = ""

            if item_count == 1:
                # Single Items

                if filename_format == 1:
                    # Uploader - Title
                    title = f"{uploaders[0]} - {titles[0]}"

                elif filename_format == 2:
                    # Title
                    title = f"{titles[0]}"

            elif item_count == 2:
                # Playlist

                if filename_format == 1:
                    # Uploader - Title
                    title = f"{uploaders[cur_item - 1]} - {titles[cur_item - 1]}"

                elif filename_format == 2:
                    # Title
                    title = f"{titles[cur_item - 1]}"

                elif filename_format == 3:
                    # Item # - Uploader - Title
                    title = f"{cur_item} - {uploaders[cur_item - 1]} - {titles[cur_item - 1]}"

                elif filename_format == 4:
                    # Item # - Title
                    title = f"{cur_item} - {titles[cur_item - 1]}"

            # Get values if downloading
            if status == "downloading" or status == "finished":
                downloaded: int = data.get("downloaded_bytes", 0)
                total: int = data.get("total_bytes") or data.get("total_bytes_estimate", 1)

                dwn_percent: float = round((downloaded / total) * 100, 1)

                # Increment current process when download is finished
                if status == "finished" and cur_process < len(titles) * 2:
                    cur_process += 1

                    # Invert status for post-processing
                    # Since all downloads also have post-processing, flip between True and False every time
                    post_processing = not post_processing

                    # Save downloaded/total when entering post-processing
                    if post_processing:
                        s_downloaded = downloaded
                        s_total = total

                    # Calculate new item value
                    new_item = ceil(cur_process / 2)

                # Move to next line if the downloaded item is completely finished
                if new_item > cur_item:

                    # Call progress callback and print new line
                    # Use the saved downloaded/total because download will only move to next item after
                    # previous item's post-processing has finished
                    if progress_callback:
                        dwn_status, cur_item = progress_callback(status, post_processing, s_downloaded, s_total,
                                                                 dwn_percent, cur_item, len(titles), title)
                    print()

                    cur_item = new_item

                # Call progress callback with no new line since cur_item hasn't changed
                elif progress_callback and post_processing:
                    dwn_status, cur_item = progress_callback(status, post_processing, s_downloaded, s_total,
                                                             dwn_percent, cur_item, len(titles), title)
                elif progress_callback:
                    dwn_status, cur_item = progress_callback(status, post_processing, downloaded, total,
                                                             dwn_percent, cur_item, len(titles), title)

        # Add progress hook for non-Artwork downloads
        if dwn_type != 3:
            ytdlp_options["progress_hooks"] = [progress_hook]

        def download_thread():
            with yt.YoutubeDL(ytdlp_options) as ydl:
                ydl.download([url])

        try:
            thread: Thread = Thread(target=download_thread)
            thread.start()

            # Wait for the download to finish
            thread.join()

            return dwn_status, cur_item

        except (yt.DownloadError, yt.DownloadCancelled) as _:
            return -1, cur_item

    @staticmethod
    def get_video_qualities(url: str) -> list[str]:
        """
        Get the available video qualities
        :param url: URL of the YouTube video
        :return: list of all available video qualities, sorted from highest to lowest
        """

        qualities: set[str] = set()
        yt_args = {
            "noplaylist": True,
            "quiet": True,
        }

        with yt.YoutubeDL(yt_args) as ydl:
            try:

                # Get formats
                info: dict = ydl.extract_info(url, download=False)

                for fmt in info.get("formats", []):
                    height: int = fmt.get("height")
                    fps: int = fmt.get("fps", 0)

                    # Skip if no height
                    if not height:
                        continue

                    # Ensure only valid video qualities are added
                    if height in VideoQuality.resolutions_30:
                        quality: str = f"{height}p"

                    elif height == 720:
                        quality: str = f"{height}p60" if fps == 60 else f"{height}p"

                    elif height == 1080:
                        quality: str = f"{height}p60" if fps == 60 else f"{height}p"

                    # Shorten 1440p and above to their common names
                    elif height == 1440:
                        quality: str = "2K60" if fps == 60 else "2K"

                    elif height == 2160:
                        quality: str = "4K60" if fps == 60 else "4K"

                    else:
                        continue

                    qualities.add(quality)

                return sorted(qualities, key=VideoQuality.resolution_sort_key, reverse=True)

            except Exception as e:
                print(f"Error: {e}")
                return []
