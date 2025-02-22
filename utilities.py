from pathlib import Path
import yt_dlp as yt


class Utilities:
    """
    Static class that contains utility functions not necessarily related yt-dlp
    """

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
