import click

from .vpc import vpc


@click.group()
def aws():
    """ Pyclops operations for AWS """


aws.add_command(vpc)
