"""
filenamecreator.py : The Filename Creator for creating custom filename formats
"""

from menu import Menu
from utilities import Utilities
from confighandler import ConfigHandler


class GetPartAt(dict):
    """
    Custom wrapper for extracting a specific part from an info dictionary
    """

    def __init__(self, *args, index=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index

    def __getitem__(self, key):
        value = super().__getitem__(key)

        # Get a part from the extracted info dictionary at a specific index
        if isinstance(value, list):
            try:
                return value[self.index]

            except IndexError:
                return ""

        return value


class FilenameCreator:
    """
    Class for creating custom filename formats
    """

    def __init__(self, dwn_mode: int = 0):
        """
        Initialize the Filename Creator
        :param dwn_mode: Download mode (1 = Single Item, 2 = Playlist, 0 = None)
        """

        self.filename_format = None
        self.dwn_mode: int = dwn_mode

        self.ch: ConfigHandler = ConfigHandler(file=Utilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()

        # TODO: When using Filename Creator from argument, get which download mode to edit for.
        # TODO: Figure out how to save default filename format using list

        # Determine which parts are available
        match self.dwn_mode:
            case 1:
                # Single Item

                self.parts: dict[str, list[str]] = Utilities.FORMAT_PARTS_S
                # self.default_format: str = self.CONFIG["default_filename_format"]["single"]

            case 2:
                # Playlist
                self.parts: dict[str, list[str]] = Utilities.FORMAT_PARTS_P
                # self.default_format: str = self.CONFIG["default_filename_format"]["playlist"]

            case _:
                # 0. No specific download mode. Combine all parts
                self.parts: dict[str, list[str]] = Utilities.FORMAT_PARTS_S | Utilities.FORMAT_PARTS_P
                # self.default_format: str = ""

        # TEMP
        # self.default_format: list[str] = ["(uploader) - (title)", "{uploader} - {title}", "%(uploader)s - %(title)s"]
        self.default_format: list[str] = ["", "", ""]

        # List: [Display Format, f-string format, yt-dlp format]
        self.current_format: list[str] = ["", "", ""]

        # Inputs
        self.custom_mode = None
        self.part_choice = None
        self.confirm = None
        self.make_default = None
        self.adv_format = None

        self.sel_part = None
        self.added_parts: list[int] = []

        # Header
        Menu.FilenameFormat.Custom.fc_header(default_format=self.default_format[0])

        # Get mode
        Menu.FilenameFormat.Custom.fc_mode()
        Menu.gap(1)

        self.custom_mode: int = Menu.Input.get_input_num(num_entries=2, default_option=1)

        match self.custom_mode:
            case 1:
                # Use presets
                self.menu_presets()
            case 2:

                # Custom format
                self.menu_custom()

    def menu_presets(self):
        while True:
            Menu.FilenameFormat.Custom.fc_simple_options(cur_format=self.current_format[0],
                                                         format_parts=self.parts, added=self.added_parts)

            options: list[str] = Utilities.menu_get_options(entries=len(self.parts))
            options += ['S', 'R']

            self.part_choice: str = Menu.Input.get_input_custom(opt_range=options, no_default=True,
                                                                invalid_opts=self.added_parts)

            # Handle menu nav
            match self.part_choice:
                case 'S':
                    # Save

                    # Handle empty format
                    if self.current_format[0] == "":
                        continue  # TODO: Display error

                    # Confirm save
                    Menu.FilenameFormat.Custom.fc_simple_confirm(cur_format=self.current_format[0])
                    Menu.gap(1)
                    self.confirm: bool = Menu.Input.get_input_bool(default_option=False)

                    if self.confirm and self.default_format[0] == "" and self.dwn_mode != 0:
                        # Prompt for default if none set. Only when used in Downloader

                        Menu.FilenameFormat.Custom.fc_make_default(cur_format=self.current_format[0],
                                                                   dwn_mode=self.dwn_mode)
                        self.make_default: bool = Menu.Input.get_input_bool(default_option=True)

                        if self.make_default:
                            # Save as default
                            self.default_format = self.current_format

                            if self.dwn_mode == 1:
                                self.CONFIG["default_filename_format"]["single"] = self.default_format

                            elif self.dwn_mode == 2:
                                self.CONFIG["default_filename_format"]["playlist"] = self.default_format

                            # TODO: Display message for setting default

                            self.ch.change_prefs(new_prefs=self.CONFIG)

                    if self.confirm and self.dwn_mode != 0:
                        # Continue with download
                        self.filename_format = list(self.current_format)
                        break

                case 'R':
                    # Reset
                    self.added_parts = []
                    self.current_format = ["", "", ""]

                    # TODO: Display message for resetting

                case _:

                    # Get format part
                    part_choice_int: int = Utilities.input_convert_to_int(input_str=self.part_choice,
                                                                          entries=len(self.parts))
                    self.sel_part: list[str] = self.parts[list(self.parts.keys())[part_choice_int - 1]]

                    # Add part to list
                    self.added_parts.append(part_choice_int)

                    # Append to current format

                    # Handle first part
                    if len(self.added_parts) == 1:
                        self.current_format[0] = list(self.parts.keys())[part_choice_int - 1]
                        self.current_format[1] = self.sel_part[0]
                        self.current_format[2] = self.sel_part[1]

                    else:
                        self.current_format[0] += f" - {list(self.parts.keys())[part_choice_int - 1]}"
                        self.current_format[1] += f" - {self.sel_part[0]}"
                        self.current_format[2] += f" - {self.sel_part[1]}"

    def menu_custom(self):
        pass
