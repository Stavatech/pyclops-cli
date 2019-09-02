import click
import inspect
import os

from pyclops.commands import cli_groups


os.environ.setdefault('BUILD_DIR', "./build")


@click.group()
def cli():
    pass

for cli_group in cli_groups:
    cli.add_command(cli_group)
