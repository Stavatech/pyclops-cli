import click

from .vpc import vpc
from .serverless import serverless


@click.group()
def aws():
    """ Pyclops operations for AWS """


aws.add_command(vpc)
aws.add_command(serverless)
