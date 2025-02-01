import yt_dlp as yt

# Globals
SCRIPT_DIR_NAME: str = "YouTube Downloads"


class Downloader:
    """
    Handles the downloading of videos, audio, and thumbnails
    Basically, all the yt-dlp functionality
    """

    # Silence yt-dlp output
    class QuietLogger:
        def debug(self, msg): pass

        def warning(self, msg): pass

        def error(self, msg): pass

    @staticmethod
    def get_title_count(url: str) -> int:
        titles: list[str] = []

        ydl_args = {
            'logger': Downloader.QuietLogger(),
            'extract_flat': True,
            'force_generic_extractor': False,
            'quiet': True,
        }

        # Extract all the titles from the URL
        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                result = ydl.extract_info(url, download=False)

                # Handle playlists
                if 'entries' in result:
                    titles = [entry.get('title', '') for entry in result['entries']]
                else:
                    titles = [result.get('title', '')]

            except Exception as e:
                print(f"Error: {e}")

        return len(titles)

    @staticmethod
    def get_playlist_name(url: str) -> str:

        ydl_args = {
            'logger': Downloader.QuietLogger(),
            'extract_flat': True,
            'force_generic_extractor': False,
            'quiet': True,
        }

        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                playlist = ydl.extract_info(url, download=False)
                return playlist['title']

            except Exception as e:
                print(f"Error: {e}")

    @staticmethod
    def setup_ytdlp_options(dwn_type: int, file_format: int, item_count: int,
                            filename_format: int, yt_url: str) -> dict:
        """
        Sets up the yt-dlp options
        :param dwn_type: Download type: 1 = Video, 2 = Audio, 3 = Artwork
        :param file_format: File format: Depends on download type
        :param item_count: Number of items: 1 = Single item, 2 = Playlist
        :param filename_format: Filename format: 1 = (uploader) - (title).(ext), 2 = (title).(ext)
        :param yt_url: YouTube URL
        :return: dictionary containing all yt-dlp options
        """

        ytdlp_options: dict = {}

        # -------------------------------------------------------------------------------
        #                               Setup Format
        # -------------------------------------------------------------------------------

        # File formats based on download type
        if dwn_type == 1:

            # Video
            if file_format == 1:
                ytdlp_options: dict = {
                    "format": "bestvideo+bestaudio",
                    "merge_output_format": "mp4"
                }

            elif file_format == 2:
                ytdlp_options: dict = {
                    "format": "bestvideo+bestaudio",
                    "merge_output_format": "mkv"
                }

            elif file_format == 3:
                ytdlp_options: dict = {
                    "format": "bestvideo+bestaudio",
                    "merge_output_format": "webm"
                }

        elif dwn_type == 2:

            # Audio
            if file_format == 1:
                ytdlp_options: dict = {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                    "audioformat": "mp3"
                }

            elif file_format == 2:
                ytdlp_options: dict = {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                    "audioformat": "vorbis"
                }

            elif file_format == 3:
                ytdlp_options: dict = {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                    "audioformat": "wav"
                }

            elif file_format == 4:
                ytdlp_options: dict = {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                    "audioformat": "flac"
                }

        elif dwn_type == 3:

            # Artwork
            if file_format == 1:
                ytdlp_options: dict = {
                    "skip_download": True,
                    "writethumbnail": True,
                    "convert_thumbnails": "png"
                }

            elif file_format == 2:
                ytdlp_options: dict = {
                    "skip_download": True,
                    "writethumbnail": True,
                    "convert_thumbnails": "jpg"
                }

        # -------------------------------------------------------------------------------
        #                               Setup Path
        # -------------------------------------------------------------------------------

        # Single item
        if item_count == 1:

            # Video
            if dwn_type == 1:

                # MP4
                if file_format == 1:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MP4/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MP4/Singles/%(title)s.%(ext)s"

                # MKV
                elif file_format == 2:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MKV/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MKV/Singles/%(title)s.%(ext)s"

                # WEBM
                elif file_format == 3:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/WEBM/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/WEBM/Singles/%(title)s.%(ext)s"

            # Audio
            elif dwn_type == 2:

                # MP3
                if file_format == 1:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/MP3/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/MP3/Singles/%(title)s.%(ext)s"

                # Vorbis
                elif file_format == 2:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/Vorbis/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/Vorbis/Singles/%(title)s.%(ext)s"

                # WAV
                elif file_format == 3:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/WAV/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/WAV/Singles/%(title)s.%(ext)s"

                # FLAC
                elif file_format == 4:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/FLAC/Singles/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options["outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/FLAC/Singles/%(title)s.%(ext)s"

            # Artwork
            elif dwn_type == 3:

                # PNG
                if file_format == 1:
                    ytdlp_options["outtmpl"] = f"~/Pictures/{SCRIPT_DIR_NAME}/PNG/Singles/%(title)s.%(ext)s"

                # JPG
                elif file_format == 2:
                    ytdlp_options["outtmpl"] = f"~/Pictures/{SCRIPT_DIR_NAME}/JPG/Singles/%(title)s.%(ext)s"

        # Playlist
        elif item_count == 2:

            # Get playlist name
            playlist_name: str = Downloader.get_playlist_name(yt_url)

            # Video
            if dwn_type == 1:

                # MP4
                if file_format == 1:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MP4/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MP4/Playlists/{playlist_name}/%(title)s.%(ext)s"

                # MKV
                elif file_format == 2:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MKV/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/MKV/Playlists/{playlist_name}/%(title)s.%(ext)s"

                # WEBM
                elif file_format == 3:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/WEBM/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Videos/{SCRIPT_DIR_NAME}/WEBM/Playlists/{playlist_name}/%(title)s.%(ext)s"

            # Audio
            elif dwn_type == 2:

                # MP3
                if file_format == 1:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/MP3/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/MP3/Playlists/{playlist_name}/%(title)s.%(ext)s"

                # Vorbis
                elif file_format == 2:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/Vorbis/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/Vorbis/Playlists/{playlist_name}/%(title)s.%(ext)s"

                # FLAC
                elif file_format == 3:

                    # (uploader) - (title).(ext)
                    if filename_format == 1:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/FLAC/Playlists/{playlist_name}/%(uploader)s - %(title)s.%(ext)s"

                    # (title).(ext)
                    elif filename_format == 2:
                        ytdlp_options[
                            "outtmpl"] = f"~/Music/{SCRIPT_DIR_NAME}/FLAC/Playlists/{playlist_name}/%(title)s.%(ext)s"

            # Artwork
            elif dwn_type == 3:

                # Uses title.ext for artwork

                # PNG
                if file_format == 1:
                    ytdlp_options[
                        "outtmpl"] = f"~/Pictures/{SCRIPT_DIR_NAME}/PNG/Playlists/{playlist_name}/%(title)s.%(ext)s"

                # JPG
                elif file_format == 2:
                    ytdlp_options[
                        "outtmpl"] = f"~/Pictures/{SCRIPT_DIR_NAME}/JPG/Playlists/{playlist_name}/%(title)s.%(ext)s"

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
            'logger': Downloader.QuietLogger(),
            'extract_flat': True,
            'force_generic_extractor': False,
            'quiet': True,
        }

        with yt.YoutubeDL(ydl_args) as ydl:
            try:
                result = ydl.extract_info(yt_url, download=False)

                # Handle playlists
                if 'entries' in result:
                    entries = result['entries']
                else:
                    entries = [result]

                # Loop through the entries and extract info
                for entry in entries:
                    titles.append(entry.get('title', 'Unknown'))
                    uploaders.append(entry.get('uploader', 'Unknown'))

                    # Only collect urls if it's a playlist
                    if item_count == 2:
                        urls.append(entry.get('webpage_url', 'Unknown'))

            except Exception as e:
                print(f"Error: {e}")

        return titles, uploaders, urls

    @staticmethod
    def download(url: str, ytdlp_options: dict) -> None:
        """
        Download an item
        :param url: YouTube URL
        :param ytdlp_options: Dictionary of yt-dlp options
        """

        with yt.YoutubeDL(ytdlp_options) as ydl:
            ydl.download([url])