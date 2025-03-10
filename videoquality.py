class VideoQuality:
    """
    Video Quality object
    """

    # Resolutions
    resolutions: dict[int, str] = {
        144: "144p",
        240: "240p",
        360: "360p",
        480: "480p",
        720: "720p",
        72060: "720p60",
        1080: "1080p",
        108060: "1080p60",
        1440: "2K",
        144060: "2K60",
        2160: "4K",
        216060: "4K60"
    }

    resolutions_30: list[int] = list(resolutions.keys())[:4]

    def __init__(self, value: str):
        self.quality: str = value
        self.is_60fps: bool = self.quality.endswith("60")

        # Validate quality
        if not self.validate_quality():
            raise VideoQuality.InvalidQuality(quality=self.quality, quality_list=list(self.resolutions.values()))

    def validate_quality(self) -> bool:
        """
        Ensures the passed quality is valid. Allows some flexibility
        :return: True if valid
        """

        if self.quality.isnumeric() and int(self.quality) in self.resolutions.keys():
            # Handle cases where the user enters a resolution without a p, and it is a key

            self.quality = self.resolutions[int(self.quality)]
            return True

        elif self.quality.upper() not in ["2K", "2K60", "4K", "4K60"]:
            self.quality = self.quality.lower()
            res: str = self.quality.split('p')[0]

            if res.isnumeric() and int(res) in self.resolutions.keys():
                # Handle cases where the user enters a resolution, with a p, that doesn't match the expected format
                # e.g. "1440p60" --> "2K60"

                if self.is_60fps and int(res) in self.resolutions_30:
                    # Don't allow qualities such as 144p60
                    return False

                self.quality = self.resolutions[int(res)] + \
                               "60" if self.is_60fps else self.resolutions[int(res)]
                return True

            elif self.quality in self.resolutions.values():
                # Handle case-insensitive user input for qualities less than 2K

                return True

            else:
                # Invalid
                return False

        elif self.quality.upper() in self.resolutions.values():
            # Handle case-insensitive user input for qualities greater than 2K

            self.quality = self.quality.upper()
            return True

        else:
            # Invalid
            return False

    @staticmethod
    def resolution_sort_key(v_quality: str) -> tuple[int, bool]:
        """
        Get the key for sorting the qualities
        :param v_quality: Video quality
        :return: Tuple of (resolution, is_60_fps), where is_60_fps is True if video is 60 fps
        """

        # Convert common names back to height
        # 2K and 4K just use '60' when they're 60 fps
        if v_quality == "4K" or v_quality == "4K60":
            resolution: int = 2160
            is_60_fps: bool = True if v_quality.endswith("60") else False

        elif v_quality == "2K" or v_quality == "2K60":
            resolution: int = 1440
            is_60_fps: bool = True if v_quality.endswith("60") else False

        # Try to get base resolution (The number before the 'p')
        elif v_quality.endswith("p60"):
            is_60_fps: bool = True

            try:
                resolution: int = int(v_quality[:-3])
            except ValueError:
                resolution: int = 0

        elif v_quality.endswith("p"):
            is_60_fps: bool = False

            try:
                resolution: int = int(v_quality[:-1])
            except ValueError:
                resolution: int = 0

        else:
            resolution: int = 0
            is_60_fps: bool = False

        return resolution, is_60_fps

    @staticmethod
    def next_best_quality(v_quality: str, available: list[str]) -> str:
        """
        Get the next best quality. e.g. 720p60 --> 720p
        :param v_quality: Video quality
        :param available: List of available qualities
        :return: Quality
        """

        non_standard: dict[str, int] = {
            "2K": 1440,
            "2K60": 144060,
            "4K": 2160,
            "4K60": 216060
        }

        # Get resolution number from quality
        resolutions: list = v_quality.lower().split('p')

        if resolutions:
            # Get resolution
            res: int = int(resolutions[0])

        elif v_quality.upper() in non_standard:
            # Quality is non-standard
            res: int = non_standard[v_quality.upper()]

        else:
            # Default to the lowest resolution if not found
            return available[-1]

        # Find the next best resolution
        for q in available:
            q_res: int = int(q.lower().split('p')[0])

            if q_res <= res:
                return q

        # Default to lowest
        return available[-1]

    class InvalidQuality(Exception):
        """
        Exception for invalid quality passed
        """

        def __init__(self, quality: str, quality_list: list[str] = None):
            super().__init__(f"Invalid quality: {quality}. Valid qualities: {', '.join(quality_list)}")
