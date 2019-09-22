import os
import click

from pyclops.lib.io import build


BUILD_DIR = os.getenv('BUILD_DIR', './build')


@click.command()
def clean():
    """ Clean the build directory """
    build.clean(BUILD_DIR)
