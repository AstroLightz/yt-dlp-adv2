"""
backend.py: The backend of the program
"""
from menu import Menu
from downloader import Downloader


class Backend:
    def __init__(self):

        # Input Vars
        self.dwn_type = None
        self.file_format = None
        self.item_count = None
        self.filename_format = None
        self.yt_url = None
        self.switch_mode = None
        self.duplicate = None

        Menu.Main.program_header()
        Menu.Main.main_menu()
        Menu.gap(1)

        self.dwn_type: int = Menu.get_input(num_entries=3, default_option=1)

        if self.dwn_type == 1:
            self.menu_video()

        elif self.dwn_type == 2:
            self.menu_audio()

        elif self.dwn_type == 3:
            self.menu_artwork()


    # ============================================================================
    #                           Menu Navigation
    # ============================================================================

    def menu_video(self):
        Menu.Video.video_menu()
        Menu.gap(1)

        self.file_format: int = Menu.get_input(num_entries=3, default_option=1)

    def menu_audio(self):
        Menu.Audio.audio_menu()
        Menu.gap(1)

        self.file_format: int = Menu.get_input(num_entries=4, default_option=1)

    def menu_artwork(self):
        Menu.Artwork.artwork_menu()
        Menu.gap(1)

        self.file_format: int = Menu.get_input(num_entries=2, default_option=1)
