import asyncio
import os
from pathlib import Path

from requests_download import download, ProgressTracker
from gwss.logger import logger

#  See if I can use requests and requests_download
async def download_file(url, dest_file: os.PathLike):
    """

    :param url: computed unpkg url
    :param dest_file: computed destination of downloaded file
    :return:
    """

    logger.debug(f"Downloading file {url} to {dest_file}")
    download(url, dest_file, trackers=ProgressTracker)
    print(f"Downloaded file {url}")