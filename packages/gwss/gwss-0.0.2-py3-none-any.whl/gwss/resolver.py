#
# UNPKG Resolver
#
# return all data needed to download scripts and styles from UNPKG
import sys
from os import PathLike
from pprint import pprint
from typing import Tuple, Dict, Any

import click
import yaml
import pathlib
from pathlib import Path

from furl import furl

from gwss.resolver_config import projects
from gwss.unpkg import Unpkg
from gwss.versions import get_latest

def resolve_pkg(package: str) -> dict[Any, Any]:
    prelim_package_version = get_latest(package=package)
    assert projects[package] is not None
    package_dict = projects[package]
    script_urls, style_urls = dict(), dict()
    if projects[package].__contains__('scripts'):
        script_urls = resolve_links(package, prelim_package_version, 'script', package_dict['dir'], package_dict['scripts'])
    if projects[package].__contains__('styles'):
        style_urls = resolve_links(package, prelim_package_version, 'style', package_dict['dir'], package_dict['styles'])
    rendered_links = dict(script_urls, **style_urls)
    package_dict['version'] = prelim_package_version
    package_dict['urls'] = rendered_links
    if package_dict.__contains__('styles'):
        del package_dict['styles']
    if package_dict.__contains__('scripts'):
        del package_dict['scripts']
    return package_dict

def resolve_links(package, version: str, s_or_s: str, dir_: PathLike, links: dict):
    """
    Returns the full url for the unpkg files in 'links'
    Parameters
    ----------

    package : str
        name of package
    version : str
        the computed version of the package
    s_or_s : str
        literal text of 'script' or 'style'
    dir_ : PathLike
        first child directory the files is in, relative to root of package
    links : dict
        A list of files to resolve

    Returns
    -------
        urls for individual files
    """
    urls = dict()
    for name, filename in links.items():
        single_unpkg_file_url = Unpkg(package, version=version, dir_=dir_, filename=filename, name=name, s_or_s=s_or_s).unpkg_url()
        if s_or_s is not None:
            if s_or_s == 'script':
                urls[f"{name}.js"] = single_unpkg_file_url
            if s_or_s == 'style':
                urls[f"{name}.css"] = single_unpkg_file_url
    return urls