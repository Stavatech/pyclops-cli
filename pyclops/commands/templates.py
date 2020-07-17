import sys
import click

from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository
from pyclops.lib.projects.project import extract_project_params, generate_from_template


DEFAULT_PROVIDER = "github"
DEFAULT_TEMPLATE = "Stavatech/Django-Template"

git_providers = {
    "github": GithubProvider() 
}


@click.group()
def templates():
    """ Template repositories are blueprints that can be used to generate new projects """


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--provider', default=DEFAULT_PROVIDER, help='The git provider of the template repository')
@click.option('--template-repo', default=DEFAULT_TEMPLATE, help='The template git repository')
@click.option('--template-params', default=None, help='Comma-separated parameters required by the specific template being used e.g. param_1=abc,param_2=def')
@click.option('--destination-repo-owner', default=None, help='The git user or organization who will own the new repository (default: omit git push)')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name:str, provider:str, template_repo:str, template_params:str, destination_repo_owner:str, working_dir:str):
    """ Generates a new project from a specified template repository """
    git_provider = git_providers[provider]
    template = git_provider.get_repo(template_repo)

    params, destination_repo_params = extract_project_params(git_provider, project_name, template_params, destination_repo_owner)

    generate_from_template(template, params, destination_repo_params, working_dir)


templates.add_command(generate_project)
