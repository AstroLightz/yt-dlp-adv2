from .utils_filenamecreator import FilenameUtilities


class MenuUtilities:
    """
    Utility functions for menu display
    """

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

    # Input/Prompts

    @staticmethod
    def input_convert_to_int(input_str: str, entries: int) -> int:
        """
        Converts the input string into an integer
        :param input_str: Input
        :param entries: Number of entries
        :return: number
        """

        if entries > 10:

            # Convert 0 to 10 and Letters to 10 + LTR
            if input_str == "0":
                choice: int = 10
            elif input_str.isalpha():
                choice: int = ord(input_str.upper()) - 54
            else:
                choice: int = int(input_str)

        elif entries > 9:

            # Convert 0 to 10
            if input_str == "0":
                choice: int = 10
            else:
                choice: int = int(input_str)

        else:

            # Convert to num
            choice: int = int(input_str)

        return choice

    @staticmethod
    def input_get_options(entries: int) -> [str, str]:
        """
        Given number of entries, format a string for input menus
        :param entries: Number of entries in menu
        :return: Formatted string [n/n+1/n+2...n+e] and max entries for error display
        """

        options: str = '['

        # Calculate the max entries string
        if entries > 10:
            # User chars
            max_entries_str: str = chr(54 + entries)

        elif entries > 9:
            # 10 entries: use 0
            max_entries_str: str = "0"

        else:
            # 1-9 entries: use the number
            max_entries_str = str(entries)

        for i in range(entries):
            if i != entries - 1:

                # If the number is less than 10, add it to the list
                if i < 9:
                    options += f"{i + 1}/"
                # If the number is 10, add 0 to the list
                elif i == 9:
                    options += "0/"

                # If the number is greater than 10, add the letter to the list (A, B, C, etc.)
                else:
                    options += f"{chr(55 + i)}/"

            else:

                if i < 9:
                    options += f"{i + 1}"
                elif i == 9:
                    options += "0"
                else:
                    options += f"{chr(55 + i)}"

        options += "]"

        return options, max_entries_str

    @staticmethod
    def menu_get_options(entries: int) -> list[str]:
        """
        Given number of entries, format a string for input menus
        :param entries: Number of entries in menu
        :return: List of each option in the menu
        """

        opt_list: list[str] = []

        for i in range(entries):
            if i < 9:
                # 1-9
                opt_list.append(f"{i + 1}")

            elif i == 9:
                # 0 for 10
                opt_list.append("0")

            else:
                # Chars after 10
                opt_list.append(f"{chr(55 + i)}")

        return opt_list

    # Confirmation Screen

    @staticmethod
    def get_download_type(dwn_type: int) -> str:
        """
        Get the download type
        :param dwn_type: Download type
        :return:
        """

        return MenuUtilities.DOWNLOAD_TYPES[dwn_type]

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
                return MenuUtilities.FILE_FORMATS["file_format_vid"][file_format]

            case 2:
                return MenuUtilities.FILE_FORMATS["file_format_aud"][file_format]

            case _:
                return MenuUtilities.FILE_FORMATS["file_format_art"][file_format]

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
            return list(FilenameUtilities.FORMAT_PRESETS_S.keys())[
                list(FilenameUtilities.FORMAT_PRESETS_S.values()).index(filename_format)]

        elif ff_mode == 1 and item_count == 2:
            # Playlist Presets
            return list(FilenameUtilities.FORMAT_PRESETS_P.keys())[
                list(FilenameUtilities.FORMAT_PRESETS_P.values()).index(filename_format)]

        else:
            # Custom: Use first item in list
            return filename_format[0]
