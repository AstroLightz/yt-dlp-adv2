"""
    All ANSI and colored-related variables
"""

from termcolor import colored as col

# Message types
SUCCESS: str = f"{col('✔', "green")}"
FAIL: str = f"{col('✘', "red")}"
INFO: str = f"{col('?', "yellow")}"
WARN: str = f"{col('⚠️', "yellow")}"
ACTION: str = f"{col('➜', "blue")}"

# ANSI Codes for input
CYAN: str = "\033[36m"
RESET: str = "\033[0m"
