import asyncio
import os
from pathlib import Path

import aiohttp
from gwss.logger import logger

async def download_file(url, dest_file: os.PathLike):
    """

    :param url: computed unpkg url
    :param dest_file: computed destination of downloaded file
    :return:
    """


    logger.debug(f"Downloading file {url} to {dest_file}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "content-disposition" in response.headers:
                header = response.headers["content-disposition"]
                file = dest_file
                with open(file, mode="wb") as file:
                    while True:
                        chunk = await response.content.read()
                        if not chunk:
                            break
                        file.write(chunk)
                print(f"Downloaded file {file}")