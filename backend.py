"""
backend.py: The backend of the program
"""
from menu import Menu
from downloader import Downloader
from sys import stdout
from wand.image import Image
from pathlib import Path


class Backend:
    def __init__(self):

        # Input Vars
        self.dwn_type = None
        self.file_format = None
        self.item_count = None
        self.filename_format = None
        self.yt_url = None
        self.switch_mode = None
        self.duplicate = None

        self.num_items = None

        # Directory Path for download
        self.download_dir = None

        # Path for actual download
        self.download_path = None

        # File extension for download
        self.file_ext = None

        self.titles: list[str] = []
        self.uploaders: list[str] = []
        self.urls: list[str] = []
        self.playlist_name: str = ""

        self.ytdlp_options: dict = {}

        Menu.Main.program_header()
        Menu.Main.main_menu()
        Menu.gap(1)

        # Download Type
        self.dwn_type: int = Menu.Input.get_input_num(num_entries=3, default_option=1)

        # File Format
        if self.dwn_type == 1:
            self.download_dir = f"{Path.home()}/Videos/YouTube Downloads/"
            self.menu_video()

        elif self.dwn_type == 2:
            self.download_dir = f"{Path.home()}/Music/YouTube Downloads/"
            self.menu_audio()

        elif self.dwn_type == 3:
            self.download_dir = f"{Path.home()}/Pictures/YouTube Downloads/"
            self.menu_artwork()

        # Item Count
        self.menu_item_count()

        # Filename Format. Default to (title).(ext) for artwork
        if self.dwn_type == 3:
            self.filename_format: int = 2
        else:
            self.menu_filename_format()

        # URL
        self.menu_get_url()

        # Download items
        self.download()

    # ============================================================================
    #                           Menu Navigation
    # ============================================================================

    ### Get file formats ###

    def menu_video(self):
        Menu.Video.video_menu()
        Menu.gap(1)

        self.file_format: int = Menu.Input.get_input_num(num_entries=3, default_option=1)

        if self.file_format == 1:
            # MP4
            self.file_ext: str = "mp4"

        elif self.file_format == 2:
            # MKV
            self.file_ext: str = "mkv"

        elif self.file_format == 3:
            # WEBM
            self.file_ext: str = "webm"

        self.download_dir += f"{self.file_ext.upper()}/"

    def menu_audio(self):
        Menu.Audio.audio_menu()
        Menu.gap(1)

        self.file_format: int = Menu.Input.get_input_num(num_entries=4, default_option=1)

        if self.file_format == 1:
            # MP3
            self.file_ext: str = "mp3"

        elif self.file_format == 2:
            # OGG
            self.file_ext: str = "ogg"

        elif self.file_format == 3:
            # WAV
            self.file_ext: str = "wav"

        elif self.file_format == 4:
            # FLAC
            self.file_ext: str = "flac"

        self.download_dir += f"{self.file_ext.upper()}/"

    def menu_artwork(self):
        Menu.Artwork.artwork_menu()
        Menu.gap(1)

        self.file_format: int = Menu.Input.get_input_num(num_entries=2, default_option=1)

        if self.file_format == 1:
            # PNG
            self.file_ext: str = "png"

        elif self.file_format == 2:
            # JPG
            self.file_ext: str = "jpg"

        self.download_dir += f"{self.file_ext.upper()}/"

    ### Get item count ###

    def menu_item_count(self):
        Menu.Main.item_count()
        Menu.gap(1)

        self.item_count: int = Menu.Input.get_input_num(num_entries=2, default_option=1)

        if self.item_count == 1:
            # Single item
            self.download_dir += "Singles/"

        elif self.item_count == 2:
            # Playlist
            self.download_dir += "Playlists/"

    ### Get filename format ###

    def menu_filename_format(self):
        Menu.Main.filename_format()
        Menu.gap(1)

        self.filename_format: int = Menu.Input.get_input_num(num_entries=2, default_option=1)

    ### Get URL ###

    def menu_get_url(self):
        Menu.Main.get_url()

        self.yt_url: str = Menu.Input.get_input_url()

    ### Download ###

    def download(self):
        """
        Set up and download items
        :return:
        """

        Menu.Download.processing_url()

        # Extract info from URL
        self.titles, self.uploaders, self.urls = Downloader.extract_info(self.item_count, self.yt_url)

        # If just a single item, add the yt url to the list
        if self.item_count == 1:
            self.urls.append(self.yt_url)

        # If a playlist, get the playlist name
        elif self.item_count == 2:
            self.playlist_name: str = Downloader.get_playlist_name(self.yt_url)

        # Set up yt-dlp options
        self.ytdlp_options = Downloader.setup_ytdlp_options(self.dwn_type, self.file_format, self.item_count,
                                                            self.download_dir, self.filename_format, self.playlist_name)

        # Get number of items
        self.num_items: int = Downloader.get_title_count(self.yt_url)

        Menu.Download.starting_download(count=self.num_items)

        # Download each item
        for i, title in enumerate(self.titles):
            Menu.Download.download_status(cur_item=i + 1, total_items=self.num_items, title=title)
            stdout.flush()

            # Construct download path
            if self.dwn_type != 3:
                if self.filename_format == 1:
                    # (uploader) - (title).(ext)
                    self.download_path = f"{self.download_dir}{self.uploaders[i]} - {title}.{self.file_ext}"
                elif self.filename_format == 2:
                    # (title).(ext)
                    self.download_path = f"{self.download_dir}{title}.{self.file_ext}"
            else:
                # yt-dlp downloads thumbnails as webp
                self.download_path = f"{self.download_dir}{title}.webp"

            dwn_status: bool = Downloader.download(self.urls[i], self.ytdlp_options)

            # If item is a thumbnail, convert to specific format
            if self.dwn_type == 3:
                Image(filename=self.download_path).convert(self.file_ext).save(
                    filename=f"{self.download_dir}{title}.{self.file_ext}")

                # Delete original thumbnail
                Path.unlink(Path(self.download_path))

            if dwn_status:
                Menu.Download.download_complete()
            else:
                Menu.Download.download_failed()

        # Menu.Main.all_downloads_complete()
        print("All downloads complete!")
