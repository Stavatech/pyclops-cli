import click

from .ecr import ecr
from .vpc import vpc
from .serverless import serverless
from .cloudformation import cloudformation


@click.group()
def aws():
    """ Pyclops operations for AWS """


aws.add_command(ecr)
aws.add_command(vpc)
aws.add_command(serverless)
aws.add_command(cloudformation)
