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

from backend import Backend
from menu import Menu, FAIL
import sys, getopt

VERSION: str = "1.4.0"
COMMITS_LINK: str = "https://github.com/AstroLightz/yt-dlp-adv2/commits/master/"


def handle_args() -> int:
    """
    Handle any arguments passed to the script
    :return: 0 If no arguments are passed, 1 if program should exit, 2 otherwise.
    """

    # h - help, v - version
    options: str = "hv"
    long_options: list[str] = ["help", "version"]

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
                Menu.Arguments.show_version(v=VERSION, g_commits=COMMITS_LINK)
                return 1

            else:
                # Assume too many arguments
                Menu.Problem.Error.error_msg(error=Exception(f"Too many arguments: Expected 1, but got {num_args}."))
                return 1

        return 0

    except getopt.error as e:
        Menu.Problem.Error.error_msg(error=Exception(f"{e}. Try 'yt-dlp-adv2 --help' for more information."))
        return 1


if __name__ == "__main__":
    try:

        # Don't execute the program if requested
        if handle_args() != 1:
            Backend()

    # Handle abrupt exits, such as CTRL+C or CTRL+D
    except (KeyboardInterrupt, EOFError):
        Menu.gap(1)
        Menu.Misc.exit_script()
