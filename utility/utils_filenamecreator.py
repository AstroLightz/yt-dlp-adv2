class FilenameUtilities:
    """
    Utilities for the FilenameCreator
    """

    # Filename format presets
    # Pair: Display Format: [f-string format, yt-dlp format]
    FORMAT_PRESETS_S: dict[str, list[str]] = {
        "(uploader) - (title).(ext)": [
            "{uploader} - {title}",
            "%(uploader)s - %(title)s.%(ext)s"
        ],

        "(title).(ext)": [
            "{title}",
            "%(title)s.%(ext)s"
        ]
    }

    FORMAT_PRESETS_P: dict[str, list[str]] = {
        "(uploader) - (title).(ext)": [
            "{uploader} - {title}",
            "%(uploader)s - %(title)s.%(ext)s"
        ],

        "(title).(ext)": [
            "{title}",
            "%(title)s.%(ext)s"
        ],

        "(item #) - (uploader) - (title).(ext)": [
            "{item_num} - {uploader} - {title}",
            "%(playlist_index)s - %(uploader)s - %(title)s.%(ext)s"
        ],

        "(item #) - (title).(ext)": [
            "{item_num} - {title}",
            "%(playlist_index)s - %(title)s.%(ext)s"
        ]
    }

    # Filename Format Parts
    # Pair: Format: [f-string format, yt-dlp format]
    FORMAT_PARTS_S: dict[str, list[str]] = {
        "(title)": [
            "{title}",
            "%(title)s"
        ],

        "(uploader)": [
            "{uploader}",
            "%(uploader)s"
        ],

        "(upload date)": [
            "{upload_date}",
            "%(upload_date)s"
        ],

        "(video id)": [
            "{id}",
            "%(id)s"
        ]
    }

    FORMAT_PARTS_P: dict[str, list[str]] = {
        "(title)": [
            "{title}",
            "%(title)s"
        ],

        "(uploader)": [
            "{uploader}",
            "%(uploader)s"
        ],

        "(item #)": [
            "{playlist_index}",
            "%(playlist_index)s"
        ],

        "(playlist name)": [
            "{playlist_title}",
            "%(playlist_title)s"
        ],

        "(playlist uploader)": [
            "{playlist_uploader}",
            "%(playlist_uploader)s"
        ]
    }

    # Playlist name presets
    PLAYLIST_NAME_PRESETS: dict[str, list[str]] = {
        "(uploader) - (title)": [
            "{uploader} - {title}",
            "%(uploader)s - %(title)s"
        ],

        "(title)": [
            "{title}",
            "%(title)s"
        ],

        "(item #) - (uploader) - (title)": [
            "{playlist_count} - {uploader} - {title}",
            "%(playlist_count)s - %(uploader)s - %(title)s"
        ],

        "(item #) - (title)": [
            "{playlist_count} - {title}",
            "%(playlist_count)s - %(title)s"
        ]
    }

    # Playlist name format parts
    PLAYLIST_NAME_FORMAT_PARTS: dict[str, list[str]] = {
        "(playlist name)": [
            "{title}",
            "%(title)s"
        ],

        "(playlist uploader)": [
            "{uploader}",
            "%(uploader)s"
        ],

        "(# Items)": [
            "{playlist_count}",
            "%(playlist_count)s"
        ],

        "(playlist id)": [
            "{id}",
            "%(id)s"
        ]
    }

    @staticmethod
    def ytdlp_to_display(ytdlp_format: str) -> list[str]:
        """
        Gets the display format and f-string format from a yt-dlp format filename format
        :param ytdlp_format: yt-dlp filename format
        :return: list of all three formats: [Display format, f-string format, yt-dlp format]
        """

        # Remove the extension
        ytdlp_format = ytdlp_format.split(".")[0]

        # Replace '%(' with '{' and ')s' with '}'
        fstring_format: str = ytdlp_format.replace("%(", "{").replace(")s", "}")

        # Replace {}s with ()s
        display_format: str = fstring_format.replace("{", "(").replace("}", ")")

        return [display_format, fstring_format, ytdlp_format]
