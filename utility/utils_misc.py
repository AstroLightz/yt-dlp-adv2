class MiscUtilities:
    """
    Miscellaneous Utilities
    """

    VERSION: str = "1.9.0"
    COMMITS_LINK: str = "https://github.com/AstroLightz/yt-dlp-adv2/commits/master/"

    UNITS: list[str] = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]

    @staticmethod
    def convert_bytes(b: int) -> str:
        """
        Convert bytes to a human-readable string
        :param b: Bytes
        :return: String with converted bytes + unit
        """

        unit_str: str = ""

        # Convert bytes to a human-readable string
        for i, unit in enumerate(MiscUtilities.UNITS):
            if b < 1024:
                # Round to 2 decimal places if not bytes
                unit_str = f"{f"{b:.2f}" if i != 0 else str(b)} {unit}B"
                break

            # Move to next unit
            b /= 1024

        return unit_str
