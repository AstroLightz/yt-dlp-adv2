"""
filenamecreator.py : The Filename Creator for creating custom filename formats
"""

from confighandler import ConfigHandler
from menu.menu_filenamecreator import FilenameMenu, PlaylistNameMenu
from menu.menu_input import Input
from menu.menu_misc import MiscMenu
from menu.menu_problems import FilenameProblem
from utility.utils_configeditor import ConfigUtilities
from utility.utils_filenamecreator import FilenameUtilities
from utility.utils_menu import MenuUtilities


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


class FCEditMode:
    """
    Edit Mode for Filename Creator
    """

    def __init__(self, edit_default: int = 0):
        self.launch_downloader = None
        self.edit_default: int | str = edit_default
        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()

        self.run()

    def pull_config(self):
        self.ch = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()

    def run(self):
        while True:
            self.pull_config()

            # Get which download mode to use
            FilenameMenu.Custom.fc_def_format(edit_format=self.edit_default,
                                              defaults=[self.CONFIG["default_filename_format"]["single"][0],
                                                        self.CONFIG["default_filename_format"]["playlist"][0],
                                                        self.CONFIG["default_playlist_name_format"][0]])
            MiscMenu.gap(1)

            # Don't allow launching the Downloader if coming from Config Editor
            if self.edit_default == -1:
                self.edit_default = Input.String.get_input_custom(opt_range=[1, 2, 3, 4, 'Q'], no_default=True)

            else:
                self.edit_default = Input.String.get_input_custom(opt_range=[1, 2, 3, 4, 'S', 'Q'],
                                                                  no_default=True)

            match str(self.edit_default):
                case '1':
                    # Single Item

                    self.edit_default = 1
                    FilenameCreator(edit_default=self.edit_default, edit_mode=True)

                case '2':
                    # Playlist

                    self.edit_default = 2
                    FilenameCreator(edit_default=self.edit_default, edit_mode=True)

                case '3':
                    # Playlist Name

                    self.edit_default = 3
                    PlaylistNameCreator(edit_mode=True)

                case '4':
                    # Clear Defaults

                    FilenameMenu.Custom.fc_clear_confirm()
                    confirm: bool = Input.Boolean.get_input_bool(default_option=False)

                    if confirm:
                        # Clear defaults
                        # Filename format
                        for k in list(self.CONFIG["default_filename_format"].keys()):
                            self.CONFIG["default_filename_format"][k].clear()
                            self.CONFIG["default_filename_format"][k].extend(["", "", ""])

                        # Playlist name format
                        self.CONFIG["default_playlist_name_format"].clear()
                        self.CONFIG["default_playlist_name_format"].extend(["", "", ""])

                        self.ch.change_prefs(new_prefs=self.CONFIG)

                        self.pull_config()

                        FilenameProblem.Success.fc_default_changed()

                case 'S':
                    # Launch Downloader
                    self.launch_downloader = True
                    return

                case 'Q':
                    # Quit
                    return


class FilenameCreator:
    """
    Class for creating custom filename formats
    """

    def __init__(self, edit_default: int = 0, edit_mode: bool = False,
                 parts: dict[str, list[str]] = None, default_format: list[str] = None, format_name: str = None):
        """
        Initialize the Filename Creator
        :param edit_default: Which default format to edit: (1 = Single Item, 2 = Playlist, 0 = Other)
        :param edit_mode: False if coming from Downloader
        :param parts: List of available parts. Required if edit default is other
        :param default_format: Default format. Required if edit default is other
        :param format_name: Name of the default format. Required if edit default is other
        """

        self.launch_downloader: bool = False

        self.filename_format = None
        self.edit_default = edit_default
        self.edit_mode = edit_mode
        self.format_name = format_name
        self.msg: str = ""

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

        self.parts = parts
        self.default_format = default_format

        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG: dict = self.ch.get_config()

        self.run()

    def run(self):
        # Determine which parts are available
        match self.edit_default:
            case 1:
                # Single Item

                self.edit_default = 1
                self.parts: dict[str, list[str]] = FilenameUtilities.FORMAT_PARTS_S
                self.default_format: list[str] = self.CONFIG["default_filename_format"]["single"]

            case 2:
                # Playlist

                self.edit_default = 2
                self.parts: dict[str, list[str]] = FilenameUtilities.FORMAT_PARTS_P
                self.default_format: list[str] = self.CONFIG["default_filename_format"]["playlist"]

            case _:
                # Other

                self.edit_default = 0

        # Header
        FilenameMenu.Custom.fc_header(default_format=self.default_format[0], edit_format=self.edit_default,
                                      edit_format_s=self.format_name)
        MiscMenu.gap(2)

        # Get mode
        FilenameMenu.Custom.fc_mode()
        MiscMenu.gap(1)

        self.custom_mode: int = Input.Integer.get_input_num(num_entries=2, default_option=1)

        match self.custom_mode:
            case 1:
                # Simple
                self.menu_simple()
            case 2:

                # Advanced
                self.menu_advanced()

    def menu_simple(self):
        while True:
            FilenameMenu.Custom.fc_simple_options(cur_format=self.current_format[0],
                                                  format_parts=self.parts, added=self.added_parts,
                                                  msg=self.msg)

            self.msg = ""

            options: list[str] = MenuUtilities.menu_get_options(entries=len(self.parts))
            options += ['S', 'R']

            self.part_choice: str = Input.String.get_input_custom(opt_range=options, no_default=True)

            # Handle menu nav
            match self.part_choice:
                case 'S':
                    # Save

                    if self.current_format[0] == "" and not self.edit_mode:
                        # Don't allow empty format outside of edit mode
                        self.msg = FilenameMenu.Messages.fc_simple_msg_empty_format()
                        continue

                    # Confirm save
                    FilenameMenu.Custom.fc_confirm(cur_format=self.current_format[0])
                    MiscMenu.gap(1)
                    self.confirm: bool = Input.Boolean.get_input_bool(default_option=False)

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

                    self.msg = FilenameMenu.Messages.fc_simple_msg_reset()

                case _:

                    # Get format part
                    part_choice_int: int = MenuUtilities.input_convert_to_int(input_str=self.part_choice,
                                                                              entries=len(self.parts))

                    # If part is already added, display error
                    if part_choice_int in self.added_parts:
                        self.msg = FilenameMenu.Messages.fc_simple_msg_part_added()
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
        while True:
            FilenameMenu.Custom.fc_adv_prompt()
            self.adv_format: str = Input.String.get_input_format()

            # Confirm save
            FilenameMenu.Custom.fc_confirm(cur_format=self.adv_format)
            MiscMenu.gap(1)
            self.confirm: bool = Input.Boolean.get_input_bool(default_option=False)

            if self.confirm:
                # Convert yt-dlp format to other formats
                self.current_format: list[str] = FilenameUtilities.ytdlp_to_display(ytdlp_format=self.adv_format)

                if self.default_format[0] == "" and not self.edit_mode:
                    # Prompt for default if none set. Only when used in Downloader
                    self.set_default()

                    # Continue with download
                    self.filename_format = list(self.current_format)
                    break

                elif not self.edit_mode:
                    # Continue with download without setting default
                    self.filename_format = list(self.current_format)
                    break

                elif self.edit_mode:
                    # Prompt for default regardless if set. Used outside of Downloader
                    self.set_default()
                    break

    def set_default(self):

        # Get config
        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()

        if not self.edit_mode:
            FilenameMenu.Custom.fc_make_default(cur_format=self.current_format[0],
                                                dwn_mode=self.edit_default,
                                                default_format=self.default_format[0])

            self.make_default: bool = Input.Boolean.get_input_bool(default_option=True)

        else:
            # Bypass if edit mode
            self.make_default = True

        if self.make_default:
            # Save as default
            self.default_format = self.current_format

            if self.edit_default == 1:
                self.CONFIG["default_filename_format"]["single"].clear()
                self.CONFIG["default_filename_format"]["single"].extend(self.default_format)

            elif self.edit_default == 2:
                self.CONFIG["default_filename_format"]["playlist"].clear()
                self.CONFIG["default_filename_format"]["playlist"].extend(self.default_format)

            FilenameProblem.Success.fc_default_changed()

            self.ch.change_prefs(new_prefs=self.CONFIG)


class PlaylistNameCreator(FilenameCreator):
    def __init__(self, edit_mode: bool = False):
        """
        Initialize PlaylistNameCreator
        :param edit_mode: False if coming from Downloader
        """
        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()
        self.edit_mode = edit_mode

        super().__init__(edit_mode=self.edit_mode, parts=FilenameUtilities.PLAYLIST_NAME_FORMAT_PARTS,
                         default_format=self.CONFIG["default_playlist_name_format"],
                         format_name="Playlist Name")

    def set_default(self):
        # Override FilenameCreator's set_default to work with just playlist name

        # Get config
        self.ch: ConfigHandler = ConfigHandler(file=ConfigUtilities.CONFIG_FILENAME)
        self.CONFIG = self.ch.get_config()

        if not self.edit_mode:
            PlaylistNameMenu.Custom.pc_make_default(cur_format=self.current_format[0],
                                                    default_format=self.default_format[0])

            self.make_default: bool = Input.Boolean.get_input_bool(default_option=True)

        else:
            # Bypass if edit mode
            self.make_default = True

        if self.make_default:
            # Save as default
            self.default_format = self.current_format

            self.CONFIG["default_playlist_name_format"].clear()
            self.CONFIG["default_playlist_name_format"].extend(self.default_format)

            FilenameProblem.Success.fc_default_changed()

            self.ch.change_prefs(new_prefs=self.CONFIG)
