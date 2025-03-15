from pathlib import Path
from typing import Any

import yt_dlp as yt
import re


class Utilities:
    """
    Static class that contains utility functions not necessarily related yt-dlp
    """

    VERSION: str = "1.9.0"
    COMMITS_LINK: str = "https://github.com/AstroLightz/yt-dlp-adv2/commits/master/"

    ## FILENAME CREATOR ##

    @staticmethod
    def get_required(filename_format: list[str]) -> dict[str, list[str]]:
        """
        Get required info needed to extract from URL
        :param filename_format: filename format list
        :return: Dictionary of part: []
        """

        format_str: str = filename_format[2]

        # Remove the extension
        format_str = format_str.split(".")[0]

        # Split on divider
        format_list: list[str] = format_str.split(" - ")

        # Remove yt-dlp formatting for each part
        # e.g. %(title)s -> title
        for i in range(len(format_list)):
            format_list[i] = re.sub(r"%\((.*?)\)s", r'\1', format_list[i], flags=re.IGNORECASE)

        # Return dict with each part as a key
        return {format_list[i]: [] for i in range(len(format_list))}

    # Filename format presets
    # Pair: Display Format: [f-string format, yt-dlp format]
    FORMAT_PRESETS_S: dict[str, list[str]] = {
        "(uploader) - (title).(ext)": [
            "{uploader} - {title}",
            "%(uploader)s - %(title)s.%(ext)s"
        ],

        "(title).(ext)": [
            "{title}",
            "%(title)s.%(ext)s"
        ]
    }

    FORMAT_PRESETS_P: dict[str, list[str]] = {
        "(uploader) - (title).(ext)": [
            "{uploader} - {title}",
            "%(uploader)s - %(title)s.%(ext)s"
        ],

        "(title).(ext)": [
            "{title}",
            "%(title)s.%(ext)s"
        ],

        "(item #) - (uploader) - (title).(ext)": [
                "{item_num} - {uploader} - {title}",
                "%(playlist_index)s - %(uploader)s - %(title)s.%(ext)s"
            ],

        "(item #) - (title).(ext)": [
            "{item_num} - {title}",
            "%(playlist_index)s - %(title)s.%(ext)s"
        ]
    }

    # Format Parts
    # Pair: Format: [f-string format, yt-dlp format]
    FORMAT_PARTS_S: dict[str, list[str]] = {
        "(title)": [
            "{title}",
            "%(title)s"
        ],

        "(uploader)": [
            "{uploader}",
            "%(uploader)s"
        ],

        "(item #)": [
            "{item_num}",
            "%(playlist_index)s"
        ],

        "(upload date)": [
            "{upload_date}",
            "%(upload_date)s"
        ],

        "(video id)": [
            "{video_id}",
            "%(id)s"
        ]
    }

    FORMAT_PARTS_P: dict[str, list[str]] = {
        "(title)": [
            "{title}",
            "%(title)s"
        ],

        "(uploader)": [
            "{uploader}",
            "%(uploader)s"
        ],

        "(item #)": [
            "{item_num}",
            "%(playlist_index)s"
        ],

        "(playlist name)": [
            "{playlist_name}",
            "%(playlist)s"
        ],

        "(playlist uploader)": [
            "{playlist_uploader}",
            "%(playlist_uploader)s"
        ],

        "(playlist id)": [
            "{playlist_id}",
            "%(playlist_id)s"
        ]
    }

    @staticmethod
    def exists_on_disk(path: str) -> bool:
        """
        Checks if a file or directory exists on the disk
        :param path: Direct path to the file or directory
        :return: True if the file or directory exists on the disk, False otherwise
        """

        return Path(path).exists()

    @staticmethod
    def delete_from_disk(path: str) -> None:
        """
        Delete a file or directory on the disk
        :param path: Direct path to the file or directory
        """

        if Path(path).is_dir():

            # Directory
            # Remove all items in the directory first
            for file in Path(path).iterdir():
                file.unlink()

            # Remove the directory
            Path(path).rmdir()

        else:

            # File
            Path(path).unlink()

    @staticmethod
    def sanitize_list(unclean_list: list[str]) -> list[str]:
        """
        Sanitize a list, replacing all invalid characters with underscores using yt-dlp's sanitation
        :param unclean_list: List to clean
        :return: Sanitized list of titles
        """

        clean_list: list[str] = []

        for item in unclean_list:
            clean_list.append(yt.utils.sanitize_filename(s=item, restricted=True))

        return clean_list

    @staticmethod
    def pref_display_value(p_value: Any) -> str:
        """
        Display the value of a preference in the Config Editor
        :param p_value: Value of the preference
        :return: Formatted string for display
        """

        if isinstance(p_value, str) and p_value == "":
            # Empty string
            return "None"

        else:
            return p_value

    @staticmethod
    def is_allowed_url(url: str, allowed_urls: list[str]) -> bool:
        """
        Checks if a URL is an allowed url in a list
        :param url: URL
        :param allowed_urls: List of allowed URLs
        :return: True if the URL is allowed, False otherwise
        """

        # Get the domain of the URL
        domain: str = url.split("/")[2]

        return domain in allowed_urls

    ## CONFIRMATION SCREEN ##

    DOWNLOAD_TYPES: dict[int, str] = {
        1: "Video",
        2: "Audio",
        3: "Artwork"
    }

    FILE_FORMATS: dict[str, dict[int, str]] = {
        "file_format_vid": {
            1: "MP4",
            2: "MKV",
            3: "WEBM"
        },
        "file_format_aud": {
            1: "MP3",
            2: "OGG",
            3: "WAV",
            4: "FLAC"
        },
        "file_format_art": {
            1: "PNG",
            2: "JPG"
        }
    }

    UNITS: list[str] = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]

    @staticmethod
    def get_download_type(dwn_type: int) -> str:
        """
        Get the download type
        :param dwn_type: Download type
        :return:
        """

        return Utilities.DOWNLOAD_TYPES[dwn_type]

    @staticmethod
    def get_file_format(file_format: int, dwn_type: int) -> str:
        """
        Get the file format
        :param file_format: file format choice
        :param dwn_type: download type choice
        :return: File extension
        """

        # Key/values for each option
        match dwn_type:
            case 1:
                return Utilities.FILE_FORMATS["file_format_vid"][file_format]

            case 2:
                return Utilities.FILE_FORMATS["file_format_aud"][file_format]

            case _:
                return Utilities.FILE_FORMATS["file_format_art"][file_format]

    @staticmethod
    def get_download_mode(item_count: int) -> str:
        """
        Get the download mode
        :param item_count: Number of items (1 = Single Item, 2 = Playlist)
        :return: Mode
        """

        return "Single Item" if item_count == 1 else "Playlist"

    @staticmethod
    def get_filename_format(item_count: int, ff_mode: int, filename_format: list[str]) -> str:
        """
        Get the filename format
        :param item_count: Number of items (1 = Single Item, 2 = Playlist)
        :param ff_mode: File format mode (Preset vs Custom)
        :param filename_format: Filename format list
        :return: Filename format key
        """

        if ff_mode == 1 and item_count == 1:
            # Single Presets
            return list(Utilities.FORMAT_PRESETS_S.keys())[
                list(Utilities.FORMAT_PRESETS_S.values()).index(filename_format)]

        elif ff_mode == 1 and item_count == 2:
            # Playlist Presets
            return list(Utilities.FORMAT_PRESETS_P.keys())[
                list(Utilities.FORMAT_PRESETS_P.values()).index(filename_format)]

        else:
            # Custom: Use first item in list
            return filename_format[0]

    ## FILE SIZE ##

    @staticmethod
    def convert_bytes(b: int) -> str:
        """
        Convert bytes to a human-readable string
        :param b: Bytes
        :return: String with converted bytes + unit
        """

        unit_str: str = ""

        # Convert bytes to a human-readable string
        for i, unit in enumerate(Utilities.UNITS):
            if b < 1024:
                # Round to 2 decimal places if not bytes
                unit_str = f"{f"{b:.2f}" if i != 0 else str(b)} {unit}B"
                break

            # Move to next unit
            b /= 1024

        return unit_str
