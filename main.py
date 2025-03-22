#!/usr/bin/env python
"""
yt-dlp-adv2: A remake of the original yt-dlp-adv, written in Python 3

main.py is the main entry point for the program
- Backend is in backend.py
- Menu print messages and input is in menu.py
- yt-dlp handling is in downloader.py
- Filename Creator is in filenamecreator.py
- Config Handling is in confighandler.py
- Utilities can be found in their respective files in the utility folder
- Menus can be found in their respective files in the menu folder

This project is licensed under the Unlicensed license. You may do whatever you want with it.
"""

import getopt
import sys

from backend import Backend
from confighandler import ConfigEditor
from filenamecreator import FCEditMode
from menu.menu_misc import MiscMenu, ArgumentMenu
from menu.menu_problems import MiscProblem
from utility.utils_misc import MiscUtilities

# Arguments
_BYPASS_DEFAULTS: bool = False


def handle_args() -> int:
    """
    Handle any arguments passed to the script
    :return: 0 If no arguments are passed, 1 if program should exit, 2 otherwise.
    """

    global _BYPASS_DEFAULTS

    options: str = "hvcfB"
    long_options: list[str] = ["help", "version", "config", "format-editor", "bypass-defaults"]

    # Get command line arguments
    cmd_args: list = sys.argv[1:]
    num_args: int = len(cmd_args)

    try:
        args, _ = getopt.getopt(cmd_args, options, long_options)

        # Check arguments
        for arg, value in args:

            if arg in ("-h", "--help") and num_args == 1:
                # Print help menu
                ArgumentMenu.help_menu()
                return 1

            elif arg in ("-v", "--version") and num_args == 1:
                # Print version
                ArgumentMenu.show_version(v=MiscUtilities.VERSION)
                ArgumentMenu.show_commits(g_commits=MiscUtilities.COMMITS_LINK)
                return 1

            elif arg in ("-c", "--config") and num_args == 1:
                # Open the Config Editor
                if ConfigEditor().launch_downloader:
                    Backend()

                return 1

            elif arg in ("-f", "--format-editor") and num_args == 1:
                # Open the Format Editor
                if FCEditMode().launch_downloader:
                    Backend()

                return 1

            elif arg in ("-B", "--bypass-defaults") and num_args == 1:
                # Bypass default preferences
                _BYPASS_DEFAULTS = True
                return 2

            else:
                # Assume too many arguments
                MiscProblem.Error.error_msg(error=Exception(f"Too many arguments: Expected 1, but got {num_args}."))
                return 1

        return 0

    except getopt.error as e:
        MiscProblem.Error.error_msg(error=Exception(f"{e}. Try 'main.py --help' for more information."))
        return 1


if __name__ == "__main__":
    try:

        # Don't execute the program if requested
        if handle_args() != 1:
            Backend(bypass_defaults=_BYPASS_DEFAULTS)

    # Handle abrupt exits, such as CTRL+C or CTRL+D
    except (KeyboardInterrupt, EOFError):
        MiscMenu.gap(1)
        MiscMenu.exit_script()
