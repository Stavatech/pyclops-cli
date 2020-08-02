import click

from pyclops.lib.docker import docker as docker_cli
from pyclops.lib.aws import ecr as ecr_utils


@click.group()
def ecr():
    """ Pyclops operations for AWS ECR """


@click.command()
@click.option('--repo-name', prompt='Repository name', help='The name that will be used for the new repo')
def create_repo(repo_name):
    """ Create an ECR repository"""
    repo_arn = ecr_utils.create_repo(repo_name)
    click.echo(repo_arn)


@click.command()
@click.option('--tag', default='latest', help='Tag the image with the given tag')
@click.option('--repository', prompt='ECR repo', help='The name of the image repository')
@click.option('--dockerfile', default='Dockerfile', help='The relative path to the Dockerfile')
def build(tag:str, repository:str, dockerfile:str):
    """ Build a Docker image from a Dockerfile """
    ecr_repo = ecr_utils.get_repo(repository)
    image = docker_cli.build_image(dockerfile, repository, tag)
    docker_cli.tag_image(image['Id'], ecr_repo['repositoryUri'], tag)


@click.command()
@click.option('--tag', default='latest', help='Tag the image with the given tag')
@click.option('--repository', prompt='ECR repo', help='The name of the image repository')
def push(tag:str, repository:str):
    """ Push a Docker image to an ECR repository """
    username, password, registry = ecr_utils.get_authorization_data()
    ecr_repo = ecr_utils.get_repo(repository)
    repository = f"{ecr_repo['repositoryUri']}:{tag}"
    docker_cli.push_image(repository, username, password, registry)


ecr.add_command(create_repo)
ecr.add_command(build)
ecr.add_command(push)
