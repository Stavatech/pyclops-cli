import click, inspect

from pyclops.commands import cli_groups


@click.group()
def cli():
    pass

for cli_group in cli_groups:
    cli.add_command(cli_group)
