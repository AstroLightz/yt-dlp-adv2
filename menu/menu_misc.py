from .menu_colors import *


class ArgumentMenu:
    """
    Contains all menus for arguments passed to the script
    """

    @staticmethod
    def help_menu() -> None:
        """
        Displays help menu
        """
        print(f"{INFO} Usage: main.py {col("[options]", "cyan")}"
              f"\n\nOptions:"
              f"\n{col("-h, --help", "cyan")}: Show this help message."
              f"\n{col("-v, --version", "cyan")}: Show script version."
              f"\n{col("-c, --config", "cyan")}: Open the Config Editor."
              f"\n{col("-f, --filename-creator", "cyan")}: Open the Filename Creator.")

    @staticmethod
    def show_version(v: str) -> None:
        """
        Displays script version
        :param v: Version string from main
        """
        print(f"{INFO} Script version: {col(v, 'cyan')}")

    @staticmethod
    def show_commits(g_commits: str) -> None:
        """
        Displays GitHub link for commits/updates
        :param g_commits: GitHub commits link
        """
        print(f"{INFO} GitHub commits: {col(g_commits, 'cyan')}")

    @staticmethod
    def defaults_bypassed() -> None:
        """
        Message to display when default preferences are bypassed
        """
        print(f"\n{INFO} Default preferences will be ignored for this session.")


class MiscMenu:
    """
    Miscellaneous menus/messages that don't fit anywhere else
    """

    @staticmethod
    def gap(length: int = 3):
        """
        Creates a gap between lines
        :param length: Number of lines between messages
        """
        print("\n" * length, end="")

    @staticmethod
    def exit_script() -> None:
        """
        Message when exiting the script, such as using CTRL+C
        """
        print(f"\n{ACTION} Exiting script...")
