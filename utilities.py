from pathlib import Path

import yt_dlp as yt


class Utilities:
    """
    Static class that contains utility functions not necessarily related yt-dlp
    """

    VERSION: str = "1.6.0"
    COMMITS_LINK: str = "https://github.com/AstroLightz/yt-dlp-adv2/commits/master/"

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

    FILENAME_FORMATS: dict[str, dict[int, str]] = {
        "filename_format_s": {
            1: "(uploader) - (title).(ext)",
            2: "(title).(ext)"
        },
        "filename_format_p": {
            1: "(uploader) - (title).(ext)",
            2: "(title).(ext)",
            3: "(item #) - (uploader) - (title).(ext)",
            4: "(item #) - (title).(ext)"
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
        if dwn_type == 1:
            return Utilities.FILE_FORMATS["file_format_vid"][file_format]
        elif dwn_type == 2:
            return Utilities.FILE_FORMATS["file_format_aud"][file_format]
        else:
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
    def get_filename_format(item_count: int, filename_format: int) -> str:
        """
        Get the filename format
        :param item_count: Number of items (1 = Single Item, 2 = Playlist)
        :param filename_format: Filename format
        :return: Filename format
        """

        if item_count == 1:
            return Utilities.FILENAME_FORMATS["filename_format_s"][filename_format]

        else:
            return Utilities.FILENAME_FORMATS["filename_format_p"][filename_format]

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
