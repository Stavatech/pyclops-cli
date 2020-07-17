import os

from pyclops.lib.jinja import jinja
from pyclops.lib.git.repo import Repository
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.io.build import clean


def extract_project_params(git_provider:GithubProvider, project_name:str, template_params:dict, destination_repo_owner:str):
    if template_params is None:
        params = {}
    else:
        params = {x[0]:x[1] for x in template_params.split(",")}
    
    params['project_name'] = project_name

    # if a destination repository owner is specified, we will create a repository in the  
    # specified account and push the generated project to that repository
    if destination_repo_owner is None:
        destination_repo_params = None
    else:
        destination_repo_params = {
            'git_owner': destination_repo_owner,
            'is_org': git_provider.is_org(params['git_owner'])
        }
    
    return params, destination_repo_params


def generate_from_template(template:Repository, params:dict, destination_repo_params:dict=None, working_dir:str="."):
    """ Generates a new project given a template repository """
    project_name = params['project_name']
    git_owner = destination_repo_params.get('git_owner') if destination_repo_params else None
    is_org = destination_repo_params.get('is_org') if destination_repo_params else None

    if git_owner:
        if 'git_owner' in params:
            raise RuntimeError("ERROR: Cannot supply 'git_owner' in --template-params when also supplying a destination repo")
        params['git_owner'] = git_owner

    # 1) make an exact copy of the template repository
    template.clone(local_dir=working_dir)
    template.remove_remote("origin")

    # 2) run jinja preprocessor to set project_name and any parameter values
    jinja.process_dir(path=working_dir, params=params, in_place=True, suffix=".pyclops", remove_suffix=True)
    template.add(path=".")
    template.commit(commit_message="Generated project according to parameters")

    # 3) push to destination repo (if provided)
    if destination_repo_params is not None:
        new_repo = template.copy_to_new(owner=git_owner, new_repo_name=project_name, is_org=is_org)

    print("\nGenerated repository: %s" % new_repo.html_url)
