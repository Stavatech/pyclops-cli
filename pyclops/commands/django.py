import sys, subprocess, click, boto3

from pyclops.lib.io import process


DEFAULT_DJANGO_TEMPLATE = "https://github.com/Stavatech/Django-Template.git"
DEFAULT_CLOUD_PROVIDER = "aws"


@click.group()
def django():
    """ Set up a Python Django application in the cloud """


@click.command()
@click.option('--name', prompt='Stack name', help='The name that will be given to the stack')
@click.option('--domain', prompt='Web domain of service', help='The domain that the service will be located at')
@click.option('--template', default=DEFAULT_DJANGO_TEMPLATE, help='The template git repository')
@click.option('--provider', default=DEFAULT_CLOUD_PROVIDER, type=click.Choice(['aws', 'azure']), help='The cloud provider to deploy the app to')
@click.argument('working-directory', type=click.Path())
def create_stack(name, domain):
    """ Command that sets up a Django stack in the cloud """
    # Steps:
    # 1) clone git repo
    out, err, returncode = process.run("git clone %s" % DEFAULT_DJANGO_TEMPLATE)
    if returncode != 0:
        print (err)
        sys.exit(returncode)

    # 2) create Docker image repo

    # 3) build and publish docker image to image repo

    
    # 4) replace cfn placeholders
    # 5) create cfn service stack
    # 6) create cfn pipeline stack


django.add_command(create_stack)
