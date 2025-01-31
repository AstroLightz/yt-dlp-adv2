#!/usr/bin/env python
"""
yt-dlp-adv2: A remake of the original yt-dlp-adv, written in Python 3

main.py is the main entry point for the program
- Backend is in backend.py
- Menu print messages and input is in menu.py
- yt-dlp handling is in downloader.py
"""

from backend import Backend

if __name__ == "__main__":
    Backend()
