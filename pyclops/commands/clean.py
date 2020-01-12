import os
import click

from pyclops.lib.io import build


@click.command()
def clean():
    """ Clean the build directory """
    build.clean(build.BUILD_DIR)
