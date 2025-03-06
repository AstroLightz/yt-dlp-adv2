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

        # Only use for video downloads
        self.video_qualities = None
        self.video_quality = None

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
        self.titles_safe: list[str] = []

        self.uploaders: list[str] = []
        self.uploaders_safe: list[str] = []

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

        # If download type is Video, ask for video quality. Does not support playlists currently.
        if self.dwn_type == 1 and self.item_count == 1:
            Menu.Video.video_quality_status()
            self.menu_video_quality()

        # Confirmation
        self.menu_confirmation()

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

    def menu_video_quality(self):

        # Get qualities
        self.video_qualities: list[str] = Downloader.get_video_qualities(self.yt_url)

        # Skip if no qualities found
        if not self.video_qualities:
            Menu.Problem.Warning.no_video_qualities()
            return

        Menu.Video.video_quality(qualities=self.video_qualities)
        Menu.gap(1)

        # Get video quality from the list
        self.video_quality: str = self.video_qualities[Menu.Input.get_input_long(
            num_entries=len(self.video_qualities), default_option=1) - 1]

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

        # Handle different filename formats prompts
        if self.item_count == 1:
            # Single item
            Menu.Main.filename_format_s()
            Menu.gap(1)

            self.filename_format: int = Menu.Input.get_input_num(
                num_entries=len(Utilities.FILENAME_FORMATS["filename_format_s"]), default_option=1)

        elif self.item_count == 2:
            # Playlist
            Menu.Main.filename_format_p()
            Menu.gap(1)

            self.filename_format: int = Menu.Input.get_input_num(
                num_entries=len(Utilities.FILENAME_FORMATS["filename_format_p"]), default_option=1)

    ### Get URL ###

    def menu_get_url(self):
        Menu.Main.get_url()

        self.yt_url: str = Menu.Input.get_input_url()

    def menu_confirmation(self):
        Menu.Main.confirmation_screen(dwn_type=self.dwn_type, file_format=self.file_format,
                                      item_count=self.item_count, filename_format=self.filename_format,
                                      video_quality=self.video_quality)

        choice: bool = Menu.Input.get_input_bool(default_option=False)

        if not choice:
            Menu.Misc.download_aborted()
            exit()

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
            elif Utilities.exists_on_disk(path=self.download_dir + self.playlist_name):

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

    # Get data from downloader and execute code based on it
    @staticmethod
    def download_callback(status: str, post_processing: bool, downloaded: int, total: int, dwn_percent: float,
                          cur_item: int, total_items: int, title: str) -> [int, int]:
        """
        Get progress from progress_hook from yt-dlp in downloader
        :param status: Download status from the progress_hook
        :param post_processing: Boolean if post-processing
        :param downloaded: Downloaded bytes
        :param total: Total bytes in download
        :param dwn_percent: Download percentage
        :param cur_item: Current item
        :param total_items: Total items
        :param title: Title of item
        """

        # Determine status int
        if status == "downloading" and post_processing:
            # Post-processing
            n_status: int = 2

        elif status == "downloading":
            # Downloading
            n_status: int = 1

        elif status == "finished":
            # Finished
            n_status: int = 0

        else:
            # Error
            n_status: int = -1

        Menu.Download.download_status(cur_item=cur_item, total_items=total_items, downloaded=downloaded,
                                      total=total, dwn_percent=dwn_percent, status=n_status, title=title)
        stdout.flush()

        return n_status, cur_item

    def construct_paths(self, cur_item: int, titles: list[str], uploaders: list[str]):
        """
        Construct download paths for non-Artwork downloads
        :param cur_item: Current item
        :param titles: List of video titles
        :param uploaders: List of uploaders
        """

        # Set index
        i: int = cur_item - 1

        if self.dwn_type != 3:
            if self.item_count == 1:
                # Single Item

                if self.filename_format == 1:
                    # (uploader) - (title).(ext)
                    self.download_path = f"{self.download_dir}{uploaders[i]} - {titles[i]}.{self.file_ext}"

                elif self.filename_format == 2:
                    # (title).(ext)
                    self.download_path = f"{self.download_dir}{titles[i]}.{self.file_ext}"

            elif self.item_count == 2:
                # Playlist

                if self.filename_format == 1:
                    # (uploader) - (title).(ext)
                    self.download_path = f"{self.download_dir}{uploaders[i]} - {titles[i]}.{self.file_ext}"

                elif self.filename_format == 2:
                    # (title).(ext)
                    self.download_path = f"{self.download_dir}{titles[i]}.{self.file_ext}"

                elif self.filename_format == 3:
                    # (item #) - (uploader) - (title).(ext)
                    self.download_path = f"{self.download_dir}{cur_item} - {uploaders[i]} - {titles[i]}.{self.file_ext}"

                elif self.filename_format == 4:
                    # (item #) - (title).(ext)
                    self.download_path = f"{self.download_dir}{cur_item} - {titles[i]}.{self.file_ext}"

    def convert_images(self, titles: list[str]):
        """
        Custom version of construct_paths for Artwork only
        :param titles: List of video titles
        """

        for i in range(len(titles)):
            # Artwork only uses title filename format

            # If item is a thumbnail, convert to specific format
            if self.item_count == 1:
                # Single Artwork
                self.download_path = f"{self.download_dir}{titles[i]}.webp"

                Image(filename=self.download_path).convert(self.file_ext).save(
                    filename=f"{self.download_dir}{titles[i]}.{self.file_ext}")

            elif self.item_count == 2:
                # Playlist Artwork
                self.download_path = f"{self.download_dir}{self.playlist_name}/{titles[i]}.webp"

                Image(filename=self.download_path).convert(self.file_ext).save(
                    filename=f"{self.download_dir}{self.playlist_name}/{titles[i]}.{self.file_ext}"
                )

            # Delete original thumbnail
            Utilities.delete_from_disk(path=self.download_path)

            # For PNG Downloads, remove any stray JPGs
            if self.file_ext.upper() == "PNG":
                if Utilities.exists_on_disk(path=self.download_path.replace(".webp", ".jpg")):
                    Utilities.delete_from_disk(path=self.download_path.replace(".webp", ".jpg"))

            # Update path
            self.download_path = f"{self.download_dir}{titles[i]}.{self.file_ext}"

            # Display status
            Menu.Download.download_status_a(cur_item=i + 1, total_items=len(titles), title=self.titles[i])

    def download(self):
        """
        Set up and download items
        :return:
        """

        Menu.Download.processing_url()

        # Get number of items
        self.num_items: int = Downloader.get_title_count(self.yt_url)

        # Extract info from URL
        self.titles, self.uploaders = Downloader.extract_info(self.yt_url)

        # Convert titles and uploaders to a safe version, replacing invalid characters with underscores
        # Save them to a new list
        self.titles_safe: list[str] = Utilities.sanitize_list(unclean_list=self.titles)
        self.uploaders_safe: list[str] = Utilities.sanitize_list(unclean_list=self.uploaders)

        # If a playlist, get the playlist name
        if self.item_count == 2:
            self.playlist_name: str = Downloader.get_playlist_name(self.yt_url)

        # Perform checks
        if not self.download_checks():
            return

        # Set up yt-dlp options
        self.ytdlp_options = Downloader.setup_ytdlp_options(dwn_type=self.dwn_type, file_format=self.file_format,
                                                            item_count=self.item_count, dwn_dir=self.download_dir,
                                                            filename_format=self.filename_format,
                                                            playlist_name=self.playlist_name,
                                                            video_quality=self.video_quality)

        Menu.Download.starting_download(count=self.num_items)

        # Download
        dwn_status, cur_item = Downloader.download(url=self.yt_url, ytdlp_options=self.ytdlp_options,
                                                   dwn_type=self.dwn_type,
                                                   item_count=self.item_count,
                                                   filename_format=self.filename_format,
                                                   titles=self.titles, uploaders=self.uploaders,
                                                   progress_callback=Backend.download_callback)

        if dwn_status == 0:
            # Download complete.

            # For non-Artwork downloads, construct download path only for Single Item downloads
            if self.dwn_type != 3 and self.item_count == 1:
                self.construct_paths(cur_item=cur_item, titles=self.titles_safe, uploaders=self.uploaders_safe)

            # For Artwork downloads, construct download path for all items
            elif self.dwn_type == 3:
                self.convert_images(titles=self.titles_safe)

        elif dwn_status == -1:
            # Download failed
            self.failed_downloads.append(self.titles_safe[cur_item])

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
