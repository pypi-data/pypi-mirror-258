import logging
import sys

import click
import colorlog

sout = click.get_text_stream('stdout')

log = logging.getLogger('GWSS')
log.setLevel(logging.DEBUG)
sout_handler = logging.StreamHandler(sout)
color_sout_handler = colorlog.StreamHandler(stream=sout)
sout_handler.setLevel(logging.DEBUG)
sout_formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
sout_handler.setFormatter(sout_formatter)
color_sout_handler.setFormatter(colorlog.ColoredFormatter(
    '%(cyan)s%(asctime)s%(reset)s:%(log_color)s%(levelname)s%(reset)s%(green)s:%(name)s%(reset)s:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'light_red',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
                                                          ))

log.addHandler(color_sout_handler)
logger = log
