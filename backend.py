"""
backend.py: The backend of the program
"""
from menu import Menu
from downloader import Downloader
from utilities import Utilities
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
        self.dwn_size = None
        self.failed_downloads: list[str] = []

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

    def download_checks(self) -> bool:
        """
        Checks to run before downloading
        :return: Boolean if all checks are passed/actions completed to mitigate errors
        """

        # Single item checks
        if self.item_count == 1:

            file_path: str = f"{self.download_dir}{self.titles[0]}.{self.file_ext}"

            # Check if URL is not a single item
            if self.num_items > 1:

                # URL is a playlist
                Menu.Problem.Warning.url_is_playlist()
                choice: bool = Menu.Input.get_input_bool(default_option=True)

                if not choice:
                    # User does not want to switch to playlist mode
                    Menu.Problem.Error.incorrect_mode_playlist()
                    return False

                else:
                    # User wants to switch to playlist mode
                    Menu.Problem.Success.mode_change_playlist()
                    self.item_count = 2
                    return True

            # Check if file already exists
            elif Utilities.exists_on_disk(path=file_path):

                # File already exists
                Menu.Problem.Warning.duplicate_single_item(title=self.titles[0])
                choice: bool = Menu.Input.get_input_bool(default_option=False)

                if choice:
                    # User wants to re-download
                    # Delete previous file
                    Menu.gap(1)
                    Menu.Download.redownloading_item(item=self.titles[0])
                    Utilities.delete_from_disk(path=file_path)
                    return True

                else:
                    # User does not want to re-download
                    Menu.Problem.Success.duplicate_single_item(path=file_path)
                    return False

        # Playlist checks
        elif self.item_count == 2:

            # Check if URL is not a playlist
            if self.num_items == 1:

                # URL is a single item
                Menu.Problem.Warning.url_is_single_item()
                choice: bool = Menu.Input.get_input_bool(default_option=True)

                if not choice:

                    # User does not want to switch to single item mode
                    Menu.Problem.Error.incorrect_mode_single()
                    return False

                else:
                    # User wants to switch to single item mode
                    Menu.Problem.Success.mode_change_single()
                    self.item_count = 1
                    return True

            # Check if playlist already exists
            elif Utilities.exists_on_disk(path=self.download_dir):

                # Playlist already exists
                Menu.Problem.Warning.duplicate_playlist(title=self.playlist_name)
                choice: bool = Menu.Input.get_input_bool(default_option=False)

                if choice:
                    # User wants to re-download
                    # Delete previous playlist
                    Menu.gap(1)
                    Menu.Download.redownloading_item(item=self.playlist_name)
                    Utilities.delete_from_disk(path=self.download_dir + self.playlist_name)
                    return True

                else:
                    # User does not want to re-download
                    Menu.Problem.Success.duplicate_playlist(path=self.download_dir)
                    return False

        # No Issues
        return True

    def download(self):
        """
        Set up and download items
        :return:
        """

        Menu.Download.processing_url()

        # Get number of items
        self.num_items: int = Downloader.get_title_count(self.yt_url)

        # Extract info from URL
        self.titles, self.uploaders, self.urls = Downloader.extract_info(self.item_count, self.yt_url)

        # If just a single item, add the yt url to the list
        if self.item_count == 1:
            self.urls.append(self.yt_url)
        # If a playlist, get the playlist name
        elif self.item_count == 2:
            self.playlist_name: str = Downloader.get_playlist_name(self.yt_url)

        # Perform checks
        if not self.download_checks():
            return

        # Set up yt-dlp options
        self.ytdlp_options = Downloader.setup_ytdlp_options(self.dwn_type, self.file_format, self.item_count,
                                                            self.download_dir, self.filename_format, self.playlist_name)

        Menu.Download.starting_download(count=self.num_items)

        # Download each item
        for i, title in enumerate(self.titles):

            # Include uploader in title if using uploader - title filename format
            if self.filename_format == 1:
                Menu.Download.download_status(cur_item=i + 1, total_items=self.num_items,
                                              title=f"{self.uploaders[i]} - {title}")
            else:
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
                self.failed_downloads.append(title)

        # Get download size. Use different path based on download type
        if self.item_count == 1:
            # Single item
            self.dwn_size: str = Downloader.get_download_size(path=self.download_path, unit="auto")

        elif self.item_count == 2:
            # Playlist
            self.dwn_size: str = Downloader.get_download_size(path=self.download_dir + self.playlist_name, unit="auto")

        Menu.Download.all_downloads_complete(completed=self.num_items, total=self.num_items,
                                             path_dir=self.download_dir, size=self.dwn_size)

        # Display failed downloads
        if len(self.failed_downloads) > 0:
            Menu.gap(1)
            Menu.Download.failed_downloads_list(failed=len(self.failed_downloads), items=self.failed_downloads)
