from typing import Any


class ConfigUtilities:
    """
    Utilities for the ConfigEditor
    """

    CONFIG_FILENAME: str = "config.yml"

    @staticmethod
    def pref_display_value(p_value: Any) -> str:
        """
        Display the value of a preference in the Config Editor
        :param p_value: Value of the preference
        :return: Formatted string for display
        """

        if isinstance(p_value, str) and p_value == "":
            # Empty string
            return "None"

        else:
            return p_value
