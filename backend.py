"""
backend.py: The backend of the program
"""
import os.path
from pathlib import Path
from sys import stdout

from wand.image import Image

from confighandler import ConfigHandler, ConfigValidator, ConfigError
from downloader import Downloader
from filenamecreator import FilenameCreator, GetPartAt

# Menus
from menu.menu_downloader import DwnMenu
from menu.menu_filenamecreator import FilenameMenu
from menu.menu_input import Input
from menu.menu_misc import MiscMenu, ArgumentMenu
from menu.menu_problems import DwnProblem, MiscProblem, ConfigProblem

# Utilities
from utility.utils_downloader import DwnUtilities
from utility.utils_filenamecreator import FilenameUtilities
from utility.utils_misc import MiscUtilities
from videoquality import VideoQuality


class Backend:
    def __init__(self, bypass_defaults: bool = False):
        """
        Backend for yt-dlp-adv2
        :param bypass_defaults: If true, will bypass any default preferences in config file.
        """

        # Argument Vars
        self.bypass_defaults = bypass_defaults

        # Input Vars
        self.dwn_type = None
        self.file_format = None
        self.item_count = None

        # Filename Format
        self.filename_format = None
        self.ff_mode = None
        self.ff_preset = None

        self.yt_url = None
        self.switch_mode = None
        self.duplicate = None

        # Only use for video downloads
        self.video_qualities = None
        self.video_quality = None

        self.num_items = None
        self.dwn_size = None
        self.failed_downloads: list[str] = []

        # Required info needed to extract
        self.required_info: dict = {}

        # Extracted info
        self.extracted_info: dict = {}

        # Sanitized info
        self.sanitized_info: dict = {}

        # Directory Path for download
        self.download_dir = None

        # Path for actual download
        self.download_path = None

        # File extension for download
        self.file_ext = None

        self.titles: list[str] = []
        self.titles_safe: list[str] = []

        self.playlist_name: str = ""

        self.ytdlp_options: dict = {}

        # Get config file
        self.ch: ConfigHandler = ConfigHandler(file="config.yml")
        self.CONFIG: dict = self.ch.get_config()

        # Validate config file
        try:
            errors: list[ConfigError] = ConfigValidator(config_handler=self.ch).config_errors

            if errors:
                # Display all errors
                ConfigProblem.Error.config_error(e=errors, config_path=self.ch.config_path)
                exit(1)

        except ConfigError as e:
            ConfigProblem.Error.config_error(e=e, config_path=self.ch.config_path)
            exit(1)

        # Display program header and version if enabled
        if self.CONFIG["show_header"]:
            DwnMenu.Main.program_header(v=MiscUtilities.VERSION if self.CONFIG["show_version"] else None)

            # Display between header and main menu if header is shown
            if self.bypass_defaults:
                ArgumentMenu.defaults_bypassed()

            else:
                MiscMenu.gap(2)

        elif self.bypass_defaults:
            # Display before main menu
            ArgumentMenu.defaults_bypassed()

        DwnMenu.Main.main_menu()
        MiscMenu.gap(1)

        # Download Type
        self.dwn_type: int = Input.Integer.get_input_num(num_entries=3, default_option=1)

        # File Format
        # Get download directory from config
        match self.dwn_type:
            case 1:
                # Video
                path: str = os.path.expandvars(os.path.expanduser(self.CONFIG["video_directory"]))

                # Remove trailing slash if it exists
                if path[-1] == "/":
                    path = path[:-1]

                self.download_dir = f"{Path(path).resolve()}/"
                self.menu_video()

            case 2:
                # Audio
                path: str = os.path.expandvars(os.path.expanduser(self.CONFIG["audio_directory"]))

                # Remove trailing slash if it exists
                if path[-1] == "/":
                    path = path[:-1]

                self.download_dir = f"{Path(path).resolve()}/"
                self.menu_audio()

            case 3:
                # Artwork
                path: str = os.path.expandvars(os.path.expanduser(self.CONFIG["artwork_directory"]))

                # Remove trailing slash if it exists
                if path[-1] == "/":
                    path = path[:-1]

                self.download_dir = f"{Path(path).resolve()}/"
                self.menu_artwork()

        # Item Count
        self.menu_item_count()

        # Filename Format.
        default_format = self.CONFIG["default_filename_format"]["single" if self.item_count == 1 else "playlist"]
        if self.bypass_defaults or not default_format[0]:

            if self.dwn_type == 3:
                # Default to (title).(ext) for artwork

                self.ff_preset: int = 2

                self.filename_format: list[str] = (
                    FilenameUtilities.FORMAT_PRESETS_S)[
                    list(FilenameUtilities.FORMAT_PRESETS_S.keys())[self.ff_preset - 1]]

                # Add key to list
                self.filename_format.insert(0, list(FilenameUtilities.FORMAT_PRESETS_S.keys())[self.ff_preset - 1])

            else:
                self.menu_filename_format()
        else:
            # Use default if present

            self.filename_format: list[str] = list(default_format)
            FilenameMenu.default_format(default_format=self.filename_format[0])

        # URL
        self.menu_get_url()

        # If download type is Video, ask for video quality. Does not support playlists currently.
        if self.dwn_type == 1 and self.item_count == 1:
            DwnMenu.Video.video_quality_status()
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
        DwnMenu.Video.video_menu()
        MiscMenu.gap(1)

        self.file_format: int = Input.Integer.get_input_num(num_entries=3, default_option=1)

        match self.file_format:
            case 1:
                # MP4
                self.file_ext: str = "mp4"

            case 2:
                # MKV
                self.file_ext: str = "mkv"

            case 3:
                # WEBM
                self.file_ext: str = "webm"

        self.download_dir += f"{self.file_ext.upper()}/"

    def menu_video_quality(self):

        # Get qualities
        self.video_qualities: list[str] = Downloader.get_video_qualities(self.yt_url)

        # Skip if no qualities found
        if not self.video_qualities:
            DwnProblem.Warning.no_video_qualities()
            return

        # If default video quality is set and is available, use it
        # Bypass if bypass defaults is enabled
        if not self.bypass_defaults:
            if self.CONFIG["default_video_quality"] and self.CONFIG["default_video_quality"] in self.video_qualities:
                self.video_quality = self.CONFIG["default_video_quality"]

                DwnMenu.Video.default_quality(quality=self.CONFIG["default_video_quality"])
                return

            elif self.CONFIG["default_video_quality"]:
                # If default video quality is set but not available, display message
                self.video_quality = VideoQuality.next_best_quality(v_quality=self.CONFIG["default_video_quality"],
                                                                    available=self.video_qualities)

                DwnProblem.Warning.default_quality_unavailable(quality=self.CONFIG["default_video_quality"],
                                                               next_quality=self.video_quality)
                return

        DwnProblem.Success.video_qualities_found(num_qualities=len(self.video_qualities))
        DwnMenu.Video.video_quality(qualities=self.video_qualities)
        MiscMenu.gap(1)

        # Get video quality from the list
        self.video_quality: str = self.video_qualities[Input.Integer.get_input_long(
            num_entries=len(self.video_qualities), default_option=1) - 1]

    def menu_audio(self):
        DwnMenu.Audio.audio_menu()
        MiscMenu.gap(1)

        self.file_format: int = Input.Integer.get_input_num(num_entries=4, default_option=1)

        match self.file_format:
            case 1:
                # MP3
                self.file_ext: str = "mp3"

            case 2:
                # OGG
                self.file_ext: str = "ogg"

            case 3:
                # WAV
                self.file_ext: str = "wav"

            case 4:
                # FLAC
                self.file_ext: str = "flac"

        self.download_dir += f"{self.file_ext.upper()}/"

    def menu_artwork(self):
        DwnMenu.Artwork.artwork_menu()
        MiscMenu.gap(1)

        self.file_format: int = Input.Integer.get_input_num(num_entries=2, default_option=1)

        match self.file_format:
            case 1:
                # PNG
                self.file_ext: str = "png"

            case 2:
                # JPG
                self.file_ext: str = "jpg"

        self.download_dir += f"{self.file_ext.upper()}/"

    ### Get item count ###

    def menu_item_count(self):
        DwnMenu.Main.item_count()
        MiscMenu.gap(1)

        self.item_count: int = Input.Integer.get_input_num(num_entries=2, default_option=1)

        match self.item_count:
            case 1:
                # Single item
                self.download_dir += "Singles/"

            case 2:
                # Playlist
                self.download_dir += "Playlists/"

    ### Get filename format ###

    def menu_filename_format(self):

        # Get type of filename format
        FilenameMenu.format_mode()
        MiscMenu.gap(1)

        self.ff_mode: int = Input.Integer.get_input_num(num_entries=2, default_option=1)

        match self.ff_mode:
            case 1:
                # Use presets

                match self.item_count:
                    case 1:
                        # Single item
                        FilenameMenu.Presets.preset_menu(presets=list(FilenameUtilities.FORMAT_PRESETS_S.keys()))
                        MiscMenu.gap(1)

                        self.ff_preset: int = Input.Integer.get_input_num(
                            num_entries=len(FilenameUtilities.FORMAT_PRESETS_S), default_option=1)

                        # Get format list from dict
                        self.filename_format: list[str] = (
                            FilenameUtilities.FORMAT_PRESETS_S)[
                            list(FilenameUtilities.FORMAT_PRESETS_S.keys())[self.ff_preset - 1]]

                        # Add filename format key to list
                        self.filename_format.insert(0,
                                                    list(FilenameUtilities.FORMAT_PRESETS_S.keys())[self.ff_preset - 1])

                    case 2:
                        # Playlist
                        FilenameMenu.Presets.preset_menu(presets=list(FilenameUtilities.FORMAT_PRESETS_P.keys()))
                        MiscMenu.gap(1)

                        self.ff_preset: int = Input.Integer.get_input_num(
                            num_entries=len(FilenameUtilities.FORMAT_PRESETS_P), default_option=1)

                        # Get format list from dict
                        self.filename_format: list[str] = (
                            FilenameUtilities.FORMAT_PRESETS_P)[
                            list(FilenameUtilities.FORMAT_PRESETS_P.keys())[self.ff_preset - 1]]

                        # Add filename format key to list
                        self.filename_format.insert(0,
                                                    list(FilenameUtilities.FORMAT_PRESETS_P.keys())[self.ff_preset - 1])

            case 2:
                # Custom

                self.filename_format: list[str] = FilenameCreator(dwn_mode=self.item_count).filename_format

    ### Get URL ###

    def menu_get_url(self):
        DwnMenu.Main.get_url()

        self.yt_url: str = Input.String.get_input_url()

    def menu_confirmation(self):
        DwnMenu.Main.confirmation_screen(dwn_type=self.dwn_type, file_format=self.file_format,
                                         item_count=self.item_count, ff_mode=self.ff_mode,
                                         filename_format=self.filename_format, video_quality=self.video_quality)

        choice: bool = Input.Boolean.get_input_bool(default_option=False)

        if not choice:
            DwnProblem.Warning.download_aborted()
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
                DwnProblem.Warning.url_is_playlist()
                choice: bool = Input.Boolean.get_input_bool(default_option=True)

                if not choice:
                    # User does not want to switch to playlist mode
                    DwnProblem.Error.incorrect_mode_playlist()
                    return False

                else:
                    # User wants to switch to playlist mode
                    DwnProblem.Success.mode_change_playlist()
                    self.item_count = 2
                    return True

            # Check if file already exists
            elif DwnUtilities.exists_on_disk(path=file_path):

                # File already exists
                DwnProblem.Warning.duplicate_single_item(title=self.titles[0])
                choice: bool = Input.Boolean.get_input_bool(default_option=False)

                if choice:
                    # User wants to re-download
                    # Delete previous file
                    MiscMenu.gap(1)
                    DwnMenu.Download.redownloading_item(item=self.titles[0])
                    DwnUtilities.delete_from_disk(path=file_path)
                    return True

                else:
                    # User does not want to re-download
                    DwnProblem.Success.duplicate_single_item(path=file_path)
                    return False

        # Playlist checks
        elif self.item_count == 2:

            # Check if URL is not a playlist
            if self.num_items == 1:

                # URL is a single item
                DwnProblem.Warning.url_is_single_item()
                choice: bool = Input.Boolean.get_input_bool(default_option=True)

                if not choice:

                    # User does not want to switch to single item mode
                    DwnProblem.Error.incorrect_mode_single()
                    return False

                else:
                    # User wants to switch to single item mode
                    DwnProblem.Success.mode_change_single()
                    self.item_count = 1
                    return True

            # Check if playlist already exists
            elif DwnUtilities.exists_on_disk(path=self.download_dir + self.playlist_name):

                # Playlist already exists
                DwnProblem.Warning.duplicate_playlist(title=self.playlist_name)
                choice: bool = Input.Boolean.get_input_bool(default_option=False)

                if choice:
                    # User wants to re-download
                    # Delete previous playlist
                    MiscMenu.gap(1)
                    DwnMenu.Download.redownloading_item(item=self.playlist_name)
                    DwnUtilities.delete_from_disk(path=self.download_dir + self.playlist_name)
                    return True

                else:
                    # User does not want to re-download
                    DwnProblem.Success.duplicate_playlist(path=self.download_dir)
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
        match status:
            case "downloading" if post_processing:
                # Post-processing
                n_status: int = 2

            case "downloading":
                # Downloading
                n_status: int = 1

            case "finished":
                # Finished
                n_status: int = 0

            case _:
                # Error
                n_status: int = -1

        DwnMenu.Download.download_status(cur_item=cur_item, total_items=total_items, downloaded=downloaded,
                                         total=total, dwn_percent=dwn_percent, status=n_status, title=title)
        stdout.flush()

        return n_status, cur_item

    def construct_paths(self, cur_item: int):
        """
        Construct download paths for non-Artwork downloads
        :param cur_item: Current item
        """

        # Set index
        i: int = cur_item - 1

        # Download path is only needed for single item downloads
        if self.dwn_type != 3 and self.item_count == 1:
            # Set download path
            # Map the filename format using the dictionary list values at i using the custom dictionary wrapper
            self.download_path = self.download_dir + self.filename_format[1].format_map(
                GetPartAt(self.sanitized_info, index=i)) + f".{self.file_ext}"

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
            DwnUtilities.delete_from_disk(path=self.download_path)

            # For PNG Downloads, remove any stray JPGs
            if self.file_ext.upper() == "PNG":
                if DwnUtilities.exists_on_disk(path=self.download_path.replace(".webp", ".jpg")):
                    DwnUtilities.delete_from_disk(path=self.download_path.replace(".webp", ".jpg"))

            # Update path
            self.download_path = f"{self.download_dir}{titles[i]}.{self.file_ext}"

            # Display status
            DwnMenu.Download.download_status_a(cur_item=i + 1, total_items=len(titles), title=self.titles[i])

    def download(self):
        """
        Set up and download items
        :return:
        """

        DwnMenu.Download.processing_download()

        # Get number of items
        self.num_items: int = Downloader.get_title_count(self.yt_url)

        # Get the required info from the filename format
        self.required_info: dict[str, list[str]] = DwnUtilities.get_required(filename_format=self.filename_format)

        # Extract info from URL
        self.extracted_info: dict[str, list[str]] = Downloader.extract_info(self.yt_url, required=self.required_info)

        # Convert all info to a safe version, replacing invalid characters with underscores
        for key, value in self.extracted_info.items():
            self.sanitized_info[key] = DwnUtilities.sanitize_list(unclean_list=value)

        if "title" in list(self.extracted_info.keys()):
            self.titles: list[str] = self.extracted_info["title"]
            self.titles_safe: list[str] = self.sanitized_info["title"]

        if not self.titles:
            # Fallback to video ID if no titles

            self.titles: list[str] = Downloader.get_video_id(url=self.yt_url)
            self.titles_safe: list[str] = DwnUtilities.sanitize_list(unclean_list=self.titles)

        # If a playlist, get the playlist name
        if self.item_count == 2:
            self.playlist_name: str = Downloader.get_playlist_name(self.yt_url)

        # Perform checks
        if not self.download_checks():
            return

        # Set up yt-dlp options
        self.ytdlp_options = Downloader.setup_ytdlp_options(dwn_type=self.dwn_type, file_format=self.file_format,
                                                            item_count=self.item_count, dwn_dir=self.download_dir,
                                                            ff_mode=self.ff_mode,
                                                            filename_format=self.filename_format,
                                                            playlist_name=self.playlist_name,
                                                            video_quality=self.video_quality)

        DwnMenu.Download.starting_download(count=self.num_items)

        # Download
        try:
            dwn_status, cur_item = Downloader.download(url=self.yt_url, ytdlp_options=self.ytdlp_options,
                                                       dwn_type=self.dwn_type,
                                                       item_count=self.item_count,
                                                       ff_mode=self.ff_preset,
                                                       filename_format=self.filename_format,
                                                       titles=self.titles,
                                                       extracted_info=self.extracted_info,
                                                       progress_callback=Backend.download_callback)

        except Exception as e:
            MiscProblem.Error.error_msg_crash(error=e)
            exit(1)

        if dwn_status == 0:
            # Download complete.

            # For non-Artwork downloads, construct download path only for Single Item downloads
            if self.dwn_type != 3 and self.item_count == 1:
                try:
                    self.construct_paths(cur_item=cur_item)

                except Exception as e:
                    MiscProblem.Error.error_msg_crash(error=e)
                    exit(1)

            # For Artwork downloads, construct download path for all items
            elif self.dwn_type == 3:
                self.convert_images(titles=self.titles_safe)

        elif dwn_status == -1:
            # Download failed
            self.failed_downloads.append(self.titles_safe[cur_item])

        # Get download size. Use different path based on download type
        try:
            match self.item_count:
                case 1:
                    # Single item
                    self.dwn_size: str = Downloader.get_download_size(path=self.download_path, unit="auto")

                case 2:
                    # Playlist
                    self.dwn_size: str = Downloader.get_download_size(path=self.download_dir + self.playlist_name,
                                                                      unit="auto")

            DwnMenu.Download.all_downloads_complete(completed=self.num_items, total=self.num_items,
                                                    path_dir=self.download_dir, size=self.dwn_size)

        except Exception as e:
            # Catch any errors when getting download size
            DwnProblem.Error.dwn_size_error(error=e)

            # Display downloads complete without size
            DwnMenu.Download.all_downloads_complete(completed=self.num_items, total=self.num_items,
                                                    path_dir=self.download_dir)

        # Display failed downloads
        if len(self.failed_downloads) > 0:
            MiscMenu.gap(1)
            DwnMenu.Download.failed_downloads_list(failed=len(self.failed_downloads), items=self.failed_downloads)
