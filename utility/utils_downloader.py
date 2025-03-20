import re
from pathlib import Path

import yt_dlp as yt


class DwnUtilities:
    """
    Utilities for the Downloader
    """

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

        # Remove yt-dlp formatting for each part
        # e.g. %(title)s -> title
        format_list = re.findall(r"%\(([^)]+)\)s", format_str)

        # Return dict with each part as a key
        return {key: [] for key in format_list}

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
            clean_list.append(yt.utils.sanitize_filename(s=str(item), restricted=True))

        return clean_list

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
