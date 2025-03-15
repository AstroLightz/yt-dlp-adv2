"""
filenamecreator.py : The Filename Creator for creating custom filename formats
"""

from confighandler import ConfigHandler
from menu import Menu
from utilities import Utilities


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
        :param dwn_mode: Download mode (1 = Single Item, 2 = Playlist, 0 = Edit Mode)
        """

        self.filename_format = None
        self.edit_mode: bool = False
        self.dwn_mode = dwn_mode
        self.msg: str = ""

        if self.dwn_mode == 0:
            self.edit_mode = True

        while True:
            self.ch: ConfigHandler = ConfigHandler(file=Utilities.CONFIG_FILENAME)
            self.CONFIG = self.ch.get_config()

            if self.edit_mode:
                # Get which download mode to use
                Menu.FilenameFormat.Custom.fc_dwn_mode(defaults=[self.CONFIG["default_filename_format"]["single"][0],
                                                                 self.CONFIG["default_filename_format"]["playlist"][0]])
                Menu.gap(1)

                self.dwn_mode: str = Menu.Input.get_input_custom(opt_range=[1, 2, 'Q'], no_default=True)

            # Determine which parts are available
            match self.dwn_mode:
                case '1':
                    # Single Item

                    self.dwn_mode = 1
                    self.parts: dict[str, list[str]] = Utilities.FORMAT_PARTS_S
                    self.default_format: list[str] = self.CONFIG["default_filename_format"]["single"]

                case '2':
                    # Playlist

                    self.dwn_mode = 2
                    self.parts: dict[str, list[str]] = Utilities.FORMAT_PARTS_P
                    self.default_format: list[str] = self.CONFIG["default_filename_format"]["playlist"]

                case 'Q':
                    # Quit. Only used in Edit Mode
                    return

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
            Menu.FilenameFormat.Custom.fc_header(default_format=self.default_format[0], dwn_mode=self.dwn_mode)
            Menu.gap(2)

            # Get mode
            Menu.FilenameFormat.Custom.fc_mode()
            Menu.gap(1)

            self.custom_mode: int = Menu.Input.get_input_num(num_entries=2, default_option=1)

            match self.custom_mode:
                case 1:
                    # Simple
                    self.menu_simple()
                case 2:

                    # Advanced
                    self.menu_advanced()

            if not self.edit_mode:
                break

    def menu_simple(self):
        while True:
            Menu.FilenameFormat.Custom.fc_simple_options(cur_format=self.current_format[0],
                                                         format_parts=self.parts, added=self.added_parts,
                                                         msg=self.msg)

            self.msg = ""

            options: list[str] = Utilities.menu_get_options(entries=len(self.parts))
            options += ['S', 'R']

            self.part_choice: str = Menu.Input.get_input_custom(opt_range=options, no_default=True)

            # Handle menu nav
            match self.part_choice:
                case 'S':
                    # Save

                    if self.current_format[0] == "" and not self.edit_mode:
                        # Don't allow empty format outside of edit mode
                        self.msg = Menu.FilenameFormat.Messages.fc_simple_msg_empty_format()
                        continue

                    # Confirm save
                    Menu.FilenameFormat.Custom.fc_simple_confirm(cur_format=self.current_format[0])
                    Menu.gap(1)
                    self.confirm: bool = Menu.Input.get_input_bool(default_option=False)

                    if self.confirm and self.default_format[0] == "" and not self.edit_mode:
                        # Prompt for default if none set. Only when used in Downloader
                        self.set_default()

                        # Continue with download
                        self.filename_format = list(self.current_format)
                        break

                    elif self.confirm and not self.edit_mode:
                        # Continue with download without setting default
                        self.filename_format = list(self.current_format)
                        break

                    elif self.confirm and self.edit_mode:
                        # Prompt for default regardless if set. Used outside of Downloader
                        self.set_default()
                        break

                case 'R':
                    # Reset
                    self.added_parts = []
                    self.current_format = ["", "", ""]

                    self.msg = Menu.FilenameFormat.Messages.fc_simple_msg_reset()

                case _:

                    # Get format part
                    part_choice_int: int = Utilities.input_convert_to_int(input_str=self.part_choice,
                                                                          entries=len(self.parts))

                    # If part is already added, display error
                    if part_choice_int in self.added_parts:
                        self.msg = Menu.FilenameFormat.Messages.fc_simple_msg_part_added()
                        continue

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

    def menu_advanced(self):
        # TODO: Add advanced menu
        pass

    def set_default(self):

        if not self.edit_mode:
            Menu.FilenameFormat.Custom.fc_make_default(cur_format=self.current_format[0],
                                                       dwn_mode=self.dwn_mode,
                                                       default_format=self.default_format[0])

            self.make_default: bool = Menu.Input.get_input_bool(default_option=True)

        else:
            # Bypass if edit mode
            self.make_default = True

        if self.make_default:
            # Save as default
            self.default_format = self.current_format

            if self.dwn_mode == 1:
                self.CONFIG["default_filename_format"]["single"] = self.default_format

            elif self.dwn_mode == 2:
                self.CONFIG["default_filename_format"]["playlist"] = self.default_format

            Menu.Problem.Success.fc_default_changed()

            self.ch.change_prefs(new_prefs=self.CONFIG)
