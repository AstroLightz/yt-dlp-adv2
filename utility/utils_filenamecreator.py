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

    # Format Parts
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
            "{playlist}",
            "%(playlist)s"
        ],

        "(playlist uploader)": [
            "{playlist_uploader}",
            "%(playlist_uploader)s"
        ],

        "(playlist id)": [
            "{playlist_id}",
            "%(playlist_id)s"
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
