import os
import sys
import subprocess
import click
import boto3

from pyclops.lib.io import process
from pyclops.lib.docker import docker
from pyclops.lib.git.github.repo import create_repo
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.template import Template


DEFAULT_DJANGO_TEMPLATE = Template(template_owner="Stavatech", template_name="Django-Template")
DEFAULT_CLOUD_PROVIDER = "aws"


@click.group()
def django():
    """ Set up a Python Django application in the cloud """


@click.command()
@click.option('--name', prompt='Stack name', help='The name that will be given to the stack')
@click.option('--domain', prompt='Web domain of service', help='The domain that the service will be located at')
@click.option('--template', default=DEFAULT_DJANGO_TEMPLATE, help='The template git repository')
@click.option('--provider', default=DEFAULT_CLOUD_PROVIDER, type=click.Choice(['aws', 'azure']), help='The cloud provider to deploy the app to')
@click.argument('working-dir', type=click.Path())
def create_stack(name, domain, template, provider, working_dir):
    """ Command that sets up a Django stack in the cloud """
    # Steps:
    # 1) clone git repo
    os.makedirs(working_dir)

    out, err, returncode = process.run("git clone %s %s" % (DEFAULT_DJANGO_TEMPLATE, working_dir))
    if returncode != 0:
        print (err)
        sys.exit(returncode)

    # 2) replace cfn placeholders

    # 3) push to new repo

    # 3) create Docker image repo
    provider_lib = __import__('pyclops.lib.aws', fromlist='')
    repo = provider_lib.docker.create_repo(name)

    # 4) build and publish docker image to image repo
    process.run('STAGE=production %s/docker/build.sh' % working_dir)

    # 5) create cfn service stack
    # 6) create cfn pipeline stack


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--owner', prompt="Git repo owner", help='The user or organization that will own the new repo')
@click.option('--template', default=DEFAULT_DJANGO_TEMPLATE, help='The template git repository')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name, owner, template, working_dir):
    """ Generates a new project from a Django template """
    # Steps:
    # 1) copy git repo to new
    os.makedirs(working_dir, exist_ok=True)
    repo = create_repo(GithubProvider(), owner, project_name, template=template)
    
    


django.add_command(create_stack)
django.add_command(generate_project)
