"""
filenamecreator.py : The Filename Creator for creating custom filename formats
"""

from menu import Menu
from utilities import Utilities


class GetPartAt(dict):
    """
    Custom wrapper for extracting a specific part from an info dictionary
    """

    def __init__(self, *args, index=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index

    def __getitem__(self, key):
        value = super().__getitem__(key)

        # Get a part from the extracted info dictionary at a specific index
        if isinstance(value, list):
            try:
                return value[self.index]

            except IndexError:
                return ""

        return value


class FilenameCreator:
    """
    Class for creating custom filename formats
    """

    def __init__(self, parts: dict[str, list[str]]):
        self.filename_format = None
        self.parts: dict[str, list[str]] = parts
