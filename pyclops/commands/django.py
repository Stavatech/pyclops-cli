import sys
import click

from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository
from pyclops.lib.projects.project import generate_from_template


DEFAULT_DJANGO_TEMPLATE = Repository(
    GithubProvider(), 
    'Stavatech', 
    'Django-Template', 
    'master', 
    'git@github.com:Stavatech/Django-Template.git', 
    'https://github.com/Stavatech/Django-Template.git'
)


@click.group()
def django():
    """ Set up a Python Django application in the cloud """


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--git-owner', prompt="Git username/organisation", help='The git username or organisation (see --is-org) that will own the new repository')
@click.option('--is-org', is_flag=True, help='Indicates whether the git owner is a user or organisation')
@click.option('--branch', default='master', help='The branch that monitored during deployments')
@click.option('--template', default=DEFAULT_DJANGO_TEMPLATE, help='The template git repository')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name:str, git_owner:str, is_org:bool, branch:str, template:Repository, working_dir:str):
    """ Generates a new project from a Django template """   
    params = {
        'project_name': project_name,
        'git_owner': git_owner,
        'git_branch': branch
    }
    generate_from_template(project_name, git_owner, is_org, branch, template, params, working_dir)


django.add_command(generate_project)
