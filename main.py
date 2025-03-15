#!/usr/bin/env python
"""
yt-dlp-adv2: A remake of the original yt-dlp-adv, written in Python 3

main.py is the main entry point for the program
- Backend is in backend.py
- Menu print messages and input is in menu.py
- yt-dlp handling is in downloader.py
- Utility functions are in utilities.py

This project is licensed under the Unlicensed license. You may do whatever you want with it.
"""

import getopt
import sys

from backend import Backend
from confighandler import ConfigEditor
from filenamecreator import FilenameCreator
from menu import Menu
from utilities import Utilities

# Arguments
_BYPASS_DEFAULTS: bool = False


def handle_args() -> int:
    """
    Handle any arguments passed to the script
    :return: 0 If no arguments are passed, 1 if program should exit, 2 otherwise.
    """

    global _BYPASS_DEFAULTS

    options: str = "hvcfB"
    long_options: list[str] = ["help", "version", "config", "filename-creator", "bypass-defaults"]

    # Get command line arguments
    cmd_args: list = sys.argv[1:]
    num_args: int = len(cmd_args)

    try:
        args, _ = getopt.getopt(cmd_args, options, long_options)

        # Check arguments
        for arg, value in args:

            if arg in ("-h", "--help") and num_args == 1:
                # Print help menu
                Menu.Arguments.help_menu()
                return 1

            elif arg in ("-v", "--version") and num_args == 1:
                # Print version
                Menu.Arguments.show_version(v=Utilities.VERSION)
                Menu.Arguments.show_commits(g_commits=Utilities.COMMITS_LINK)
                return 1

            elif arg in ("-c", "--config") and num_args == 1:
                # Open the Config Editor
                if ConfigEditor().launch_downloader:
                    Backend()

                return 1

            elif arg in ("-f", "--filename-creator") and num_args == 1:
                # Open the Filename Creator
                FilenameCreator()

                return 1

            elif arg in ("-B", "--bypass-defaults") and num_args == 1:
                # Bypass default preferences
                _BYPASS_DEFAULTS = True
                return 2

            else:
                # Assume too many arguments
                Menu.Problem.Error.error_msg(error=Exception(f"Too many arguments: Expected 1, but got {num_args}."))
                return 1

        return 0

    except getopt.error as e:
        Menu.Problem.Error.error_msg(error=Exception(f"{e}. Try 'main.py --help' for more information."))
        return 1


if __name__ == "__main__":
    try:

        # Don't execute the program if requested
        if handle_args() != 1:
            Backend(bypass_defaults=_BYPASS_DEFAULTS)

    # Handle abrupt exits, such as CTRL+C or CTRL+D
    except (KeyboardInterrupt, EOFError):
        Menu.gap(1)
        Menu.Misc.exit_script()
