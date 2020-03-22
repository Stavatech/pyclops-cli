import click

from pyclops.lib.aws.ecr import create_repo as create_ecr_repo


@click.group()
def ecr():
    """ Pyclops operations for AWS ECR """


@click.command()
@click.option('--repo-name', prompt='Repository name', help='The name that will be used for the new repo')
def create_repo(repo_name):
    repo_arn = create_ecr_repo(repo_name)
    click.echo(repo_arn)


ecr.add_command(create_repo)
