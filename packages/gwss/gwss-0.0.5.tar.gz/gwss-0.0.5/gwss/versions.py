from typing import Union
from lastversion import latest
def get_latest(package: str) -> str:
    version: str = latest(package, output_format='tag')
    if version[0] == 'v':
        version = version[1:]
    assert version is not None
    return version