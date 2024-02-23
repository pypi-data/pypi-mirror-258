import asyncio
from os import PathLike
from typing import Any

import click

from gwss.download import download_file
from gwss import resolver
from furl import furl, Fragment

from gwss.logger import logger


class Unpkg:

    base_url = furl('https://unpkg.com')

    def __init__(self,
                 package: str,
                 version: str,
                 dir_: PathLike | None,
                 name: PathLike,
                 filename: PathLike,
                 s_or_s: str | None) -> object:
        """

        Args:
            package : str
                The package name
            version : str
                The version number of the package
            dir_ : str | PathLike | None
                root (dir)ectory that downloadable files are in (umd|dist|.)
                If isn't needed (if results are already pulled) should be left out
            name : str | PathLike
                The 'nickname' given to the file to save as
            filename : str | PathLike
                The first parent directory and filename of wanted file (without extension)
            s_or_s : str
                The string 'scripts' or 'styles'




        """
        self.package = package
        self.version = version
        self.dir_ = dir_
        self.name = name
        self.filename = filename
        self.s_or_s = s_or_s
        self.url = ''


    def unpkg_dl(self, url, dest_file: PathLike) -> bool | Any:
        """
        Download the package file from unpkg.com
        Parameters
        ----------
        url : furl | str | None
            url to download from
        dest_file : str | PathLike
            local file to download to

        Returns
        -------
        True if files are successfully downloaded
        False otherwise
        """
        logger.debug(f"Downloading files from Unpkg")
        logger.debug(f'Trying to download {self.unpkg_url()} to {dest_file}')
        asyncio.run(download_file(url=self.unpkg_url(), dest_file=dest_file))


    def unpkg_url(self) -> furl:
        """
        Create a URL using the base URL, package, version, directory, file,
        and extension.

        :return:
        :param args: Positional arguments for directory and file.
        :param kwargs: Keyword arguments for directory and file.
        :return: The created URL as a string.
        """
        url = furl(self.base_url)
        # create url
        package = self.package
        url = url.add(path=f"{package}")
        version = self.version
        url = furl(f'{url.url}@{version}')
        _dir = self.dir_
        url = url.add(path=f"{_dir}")
        file = self.filename
        url = url.add(path=f"{file}")
        self.url = url.path.normalize()
        return url