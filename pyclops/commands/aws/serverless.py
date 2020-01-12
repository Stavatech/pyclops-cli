import os
import sys
import click

from pyclops.lib.jinja import jinja
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository
from pyclops.lib.io.build import clean


DEFAULT_SERVERLESS_TEMPLATE = Repository(
    GithubProvider(), 
    'Stavatech', 
    'AWS-Serverless-Template', 
    'master', 
    'git@github.com:Stavatech/AWS-Serverless-Template', 
    'https://github.com/Stavatech/VPC-Template.git'
)


@click.group()
def serverless():
    """ Pyclops operations for AWS VPC """


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--git-owner', prompt="Git username/organisation", help='The git username or organisation (see --is-org) that will own the new repository')
@click.option('--is-org', is_flag=True, help='Indicates whether the git owner is a user or organisation')
@click.option('--branch', default='master', help='The branch that monitored during deployments')
@click.option('--template', default=DEFAULT_SERVERLESS_TEMPLATE, help='The template git repository')
@click.option('--deployment-bucket', prompt="S3 deployment bucket", help='The bucket the deploymjent artifacts will be sent to when deploying with SAM-CLI')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name:str, git_owner:str, is_org:bool, branch:str, template:Repository, deployment_bucket:str, working_dir:str):
    """ Generates a new project from an AWS Serverless template """   
    # Steps:     
    # 1) copy template repo
    template_dir = os.path.join(working_dir, "template")
    template.clone(local_dir=template_dir)

    new_repo = template.copy_to_new(owner=git_owner, new_repo_name=project_name, is_org=is_org)

    clean(path=template_dir)

    # 2) clone new repo
    new_repo.clone(local_dir=working_dir)

    # 3) run jinja preprocessor to set project_name
    params = {
        'project_name': project_name,
        'git_owner': git_owner,
        'git_branch': branch,
        'sam_deploy_bucket': deployment_bucket
    }
    jinja.process_dir(path=working_dir, params=params, in_place=True, suffix=".pyclops", remove_suffix=True)

    # 3) push the processed repo to remote
    new_repo.add(path=".")
    new_repo.commit(commit_message="Generated project according to parameters")
    new_repo.push()

    print("\nGenerated repository: %s" % new_repo.html_url)


serverless.add_command(generate_project)