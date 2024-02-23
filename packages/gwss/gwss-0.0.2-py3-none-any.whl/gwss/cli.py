from importlib.metadata import version as i_version
import sys
import os
from pathlib import Path
from pprint import pprint

import click
from click import Context

from gwss import gwss, resolver_config
from gwss.config import config
from gwss.resolver import resolve_pkg
from gwss.unpkg import Unpkg
from gwss.utilities import prepare_config, path_validation, squish_info, path_create


class Site(object):
    last_result = None
    dest_dir = None
    def __init__(self, destination_directory, last_result=None):
        self.dest_dir = os.path.abspath(destination_directory or '.')
        self.last_result = None or last_result

    def __enter__(self):
        self.last_result = self.last_result
    def __exit__(self, exc_type, exc_value, tb):
        #self.last_result
        pass
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("v{}".format(i_version('gwss')))
    ctx.exit()

@click.group(invoke_without_command=True, chain=True)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=False)
@click.option('--dest-dir', '-d', default='.site', type=Path)

@click.pass_context
def cli(ctx, dest_dir, last_result=None):
    ctx.obj = ctx.with_resource(Site(destination_directory=dest_dir, last_result=last_result))
    pass

@cli.command(name='list', help="list the script and style names from the '{}' file".format(Path.joinpath(Path.home(), '.gwss')))
def ls():
    cfg = prepare_config(config)
    print(cfg)

@cli.command(help="get all urls and destination directories for styles and scripts")
@click.option('--dest-dir', '-d', default='.site', type=Path)
@click.pass_context
def resolve(ctx, dest_dir):
    resolve_rendered = {}
    for root, projects in config.items():
        for v_ in projects:
            package_dict = resolve_pkg(v_)
            resolve_rendered[v_] = package_dict
    Site.last_result = resolve_rendered
    return resolve_rendered

@cli.command()
@click.option('--dest-dir', '-d', default=Path('./site_files'), type=Path)
@click.pass_context
def download(_ctx, dest_dir: Path | os.PathLike):
    if Site.last_result is not None:
        result = Site.last_result
        if path_validation(dest_dir):
            pass
        else:
            path_create(dest_dir)
        click.echo(f'Downloading all needed scripts and styles to {dest_dir}')
        for project, dict_ in result.items():
            version = dict_['version']
            urls = dict_['urls']
            dir_ = dict_['dir']
            pprint(urls)
            for name, url_ in urls.items():
                pprint(f"{name} -> {url_}")
                name_file = name.split('.')[0]
                name_ext = name.split('.')[1]
                dest_file = Path(os.getcwd()).joinpath(dest_dir, f"{name_file}-{version}.{name_ext}")
                pprint(dest_file)
                file_ = Unpkg(project, version, dir_, name, name, None)
                file_.unpkg_dl(url_, dest_file)
    else:
        click.secho(f"No previous results to use, use 'gwss resolve download'", err=True)



