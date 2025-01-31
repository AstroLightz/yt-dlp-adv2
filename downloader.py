import yt_dlp as yt
from pathlib import Path

# Globals
SCRIPT_DIR_NAME: str = "YouTube Downloads"


class Downloader:
    """
    Handles the downloading of videos, audio, and thumbnails
    Basically, all the yt-dlp functionality
    """

    @staticmethod
    def get_title_count(url: str) -> int:
        titles: list[str] = []

        # Silence output. Don't need it here
        class QuietLogger:
            def debug(self, msg): pass
            def warning(self, msg): pass
            def error(self, msg): pass

        ydl_args = {
            'logger': QuietLogger(),
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


    def __init__(self, url: str, dwn_type: int, file_format: int, item_count: int, filename_format: int):
        self.url = url
        self.dwn_type = dwn_type
        self.file_format = file_format
        self.item_count = item_count
        self.filename_format = filename_format

        self.format = None
        self.dwn_path = None

        # Setups
        self.setup_format()
        self.setup_path()

    def setup_format(self) -> None:
        """
        Sets up the formatting for the yt-dlp command
        """

        # File formats based on download type
        if self.dwn_type == 1:

            # Video
            if self.file_format == 1:
                self.format: str = "-f bestvideo+bestaudio --merge-output-format mp4"
            elif self.file_format == 2:
                self.format: str = "-f bestvideo+bestaudio --merge-output-format mkv"
            elif self.file_format == 3:
                self.format: str = "-f bestvideo+bestaudio --merge-output-format webm"

        elif self.dwn_type == 2:

            # Audio
            if self.file_format == 1:
                self.format: str = "-x --audio-format mp3"
            elif self.file_format == 2:
                self.format: str = "-x --audio-format vorbis"
            elif self.file_format == 3:
                self.format: str = "-x --audio-format wav"
            elif self.file_format == 4:
                self.format: str = "-x --audio-format flac"

        elif self.dwn_type == 3:

            # Artwork
            if self.file_format == 1:
                self.format: str = "--skip-download --write-thumbnail --convert-thumbnails png"
            elif self.file_format == 2:
                self.format: str = "--skip-download --write-thumbnail --convert-thumbnails jpg"

    def setup_path(self) -> None:
        """
        Set up the download path for the item(s).
        """

        # Determine target directory
        if self.dwn_type == 1:
            # Video
            self.dwn_path: Path = Path(f"~/Videos/{SCRIPT_DIR_NAME}").expanduser()

            if self.file_format == 1:
                # MP4
                self.dwn_path: Path = self.dwn_path / "MP4"

            elif self.file_format == 2:
                # MKV
                self.dwn_path: Path = self.dwn_path / "MKV"

            elif self.file_format == 3:
                # WEBM
                self.dwn_path: Path = self.dwn_path / "WEBM"

        elif self.dwn_type == 2:
            # Audio
            self.dwn_path: Path = Path(f"~/Music/{SCRIPT_DIR_NAME}").expanduser()

            if self.file_format == 1:
                # MP3
                self.dwn_path: Path = self.dwn_path / "MP3"

            elif self.file_format == 2:
                # OGG
                self.dwn_path: Path = self.dwn_path / "OGG"

            elif self.file_format == 3:
                # WAV
                self.dwn_path: Path = self.dwn_path / "WAV"

            elif self.file_format == 4:
                # FLAC
                self.dwn_path: Path = self.dwn_path / "FLAC"

        elif self.dwn_type == 3:
            # Artwork
            self.dwn_path: Path = Path(f"~/Pictures/{SCRIPT_DIR_NAME}").expanduser()

            if self.file_format == 1:
                # PNG
                self.dwn_path: Path = self.dwn_path / "PNG"

            elif self.file_format == 2:
                # JPG
                self.dwn_path: Path = self.dwn_path / "JPG"

        # Create the script download directory if it doesn't exist
        self.dwn_path.mkdir(parents=True, exist_ok=True)
