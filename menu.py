from termcolor import colored

# Message types
SUCCESS: str = f"{colored('✔', "green")}"
FAIL: str = f"{colored('✘', "red")}"
INFO: str = f"{colored('?', "yellow")}"
WARN: str = f"{colored('⚠️', "yellow")}"
ACTION: str = f"{colored('➜', "blue")}"


class Menu:
    """
    Contains all menus for the program
    """

    @staticmethod
    def gap(length: int = 3):
        """
        Creates a gap between lines
        :param length: Number of lines between messages
        """
        print("\n" * length, end="")

    @staticmethod
    def get_input(num_entries: int = 3, default_option: int = 1) -> int:
        """
        Gets input from the user
        :param default_option: The default option to select
        :param num_entries: Number of entries in the menu. Must be at least 2
        :return: The selected option
        """

        # Create options list string
        options_list: str = "["

        for i in range(num_entries):
            if i != num_entries - 1:
                options_list += f"{i + 1}/"
            else:
                options_list += f"{i + 1}"

        options_list += "]"

        while True:
            try:
                choice: int = int(
                    input(f"> {colored(options_list, "magenta")} {colored(f"({default_option})", "cyan")}: ") or default_option)

                if choice < 1 or choice > num_entries:
                    raise ValueError

                return choice

            except ValueError:
                print(f"{FAIL} {colored(f"Invalid input. Please enter an integer between 1 and {num_entries}.", "red")}")

    class Main:
        """
        Contains all menus that are not specific to any particular download type
        """

        @staticmethod
        def program_header():
            print(f"\nWelcome to {colored("YouTube Downloader: Advanced 2.0!", "red")}!")
            print(
                f"{colored("A remake of the original yt-dlp-adv, written in Python. Now with new features!", 'green')}\n")

            print(
                f"{colored('●', "red")} This is a ZSH script that simplifies the use of the "
                f"{colored("yt-dlp", "red")} tool ({colored("https://github.com/yt-dlp/yt-dlp", "cyan")}).")
            print(
                f"{colored('●', "red")} It provides a user-friendly, menu-driven interface to help you "
                f"download videos, audio, and thumbnails from YouTube and other platforms.")
            print(
                f"{colored('●', "red")} You can easily customize download options and formats without "
                f"needing to remember complex command-line arguments.")
            print(f"{colored('●', "red")} The script supports downloading entire playlists or single items.")
            print(f"{colored('●', "red")} It also offers detailed feedback on the download status and file sizes.\n")
            print(
                f"{colored('●', "magenta")} I designed this script to be straightforward and user-friendly "
                f"for people who, like me, don't have a lot of time to look up-")
            print(f"{colored('●', "magenta")} complex commands and just need a quick way to download content.\n")
            print(f"{colored('●', "yellow")} Script made by {colored("AstroLightz", "cyan")}. I hope you enjoy!\n\n")

        @staticmethod
        def main_menu():
            """
            Displays list of download types
            """
            print(f"\n{INFO} What would you like to download?")
            print(f"  {colored('1', "cyan")}) Videos")
            print(f"  {colored('2', "cyan")}) Audio")
            print(f"  {colored('3', "cyan")}) Thumbnails")

    class Video:
        """
        Contains all menus for video downloads
        """
        
        @staticmethod
        def video_menu():
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {colored('1', "cyan")}) MP4")
            print(f"  {colored('2', "cyan")}) MKV")
            print(f"  {colored('3', "cyan")}) WEBM")

    class Audio:
        """
        Contains all menus for audio downloads
        """

        @staticmethod
        def audio_menu():
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {colored('1', "cyan")}) MP3")
            print(f"  {colored('2', "cyan")}) OGG")
            print(f"  {colored('3', "cyan")}) WAV")
            print(f"  {colored('4', "cyan")}) FLAC")

    class Artwork:
        """
        Contains all menus for artwork/thumbnail downloads
        """

        @staticmethod
        def artwork_menu():
            print(f"\n{INFO} What file format do you want to use?")
            print(f"  {colored('1', "cyan")}) PNG")
            print(f"  {colored('2', "cyan")}) JPG")
