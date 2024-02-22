# -*- encoding: utf-8 -*-
import os
import platform
from pathlib import Path


class OsUtils:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def get_os_name() -> str:
        """
        Get OS name
        :return:
        """

        return platform.system()

    @staticmethod
    def is_windows() -> bool:
        """
        Check if OS is Windows
        :return:
        """

        return True if platform.system().lower() == "windows" else False

    @staticmethod
    def get_current_path() -> Path | None:
        """
        Returns the current working directory
        :return: Path
        """

        path = os.path.abspath(os.getcwd())
        return Path(os.path.normpath(path)) if path else None

    def get_pictures_path(self) -> Path:
        """
        Returns the pictures directory inside the user's home directory
        :return: Path
        """

        if self.is_windows():
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            pictures_guid = "My Pictures"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                pictures_path = winreg.QueryValueEx(key, pictures_guid)[0]
            return Path(pictures_path)
        else:
            pictures_path = os.path.join(os.getenv("HOME"), "Pictures")
            return Path(pictures_path)

    def get_downloads_path(self) -> Path:
        """
        Returns the download directory inside the user's home directory
        :return: Path
        """

        if self.is_windows():
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
            return Path(downloads_path)
        else:
            downloads_path = os.path.join(os.getenv("HOME"), "Downloads")
            return Path(downloads_path)
