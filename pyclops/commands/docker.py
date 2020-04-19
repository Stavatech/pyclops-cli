import sys
import click

from pyclops.lib.docker import docker as docker_cli
from pyclops.lib.aws import ecr


@click.group()
def docker():
    """ Docker wrapper commands """


@click.command()
@click.option('--tag', default='latest', help='Tag the image with the given tag')
@click.option('--repository', default='latest', help='The name of the image repository')
@click.option('--dockerfile', default='Dockerfile', help='The relative path to the Dockerfile')
def build(tag:str, repository:str, dockerfile:str):
    """ Build a Docker image from a Dockerfile """
    docker_cli.build_image(dockerfile, repository, tag)


@click.command()
@click.option('--tag', default='latest', help='Tag the image with the given tag')
@click.option('--repository', prompt='Repository', help='The name of the image repository')
@click.option('--image-id', prompt='Image ID', help='The ID of the image to tag')
def tag(tag:str, repository:str, image_id:str):
    """ Tag a Docker image """
    docker_cli.tag_image(image_id, repository, tag)


@click.command()
@click.option('--tag', default='latest', help='Tag the image with the given tag')
@click.option('--repository', default='latest', help='The name of the image repository')
def push(tag:str, repository:str):
    """ Push a Docker image to a repository """
    username, password, registry = ecr.get_authorization_data()
    registry = registry[8:]
    print(f"{registry}/{repository}:{tag}")
    docker_cli.push_image(f"{registry}/{repository}:{tag}", username, password, registry)


docker.add_command(build)
docker.add_command(tag)
docker.add_command(push)
