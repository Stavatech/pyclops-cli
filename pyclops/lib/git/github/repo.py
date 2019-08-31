import os
import requests
from pyclops.lib.git.template import Template
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository


def create_repo(git_provider:GithubProvider, owner:str, name:str, is_org:bool=False, optional_params:dict={}, template:Template=None) -> Repository:
    if template is not None:
        body = {"name": name, "owner": owner, **optional_params}  
        relative_url = "repos/%s/%s/generate" % (template.template_owner, template.template_name)
    else:
        body = {"name": name, **optional_params}        
        if is_org:
            relative_url = "orgs/%s/repos" % owner
        else:
            relative_url = "%s/repos" % owner
    
    headers = {
        "Authorization": "token %s" % git_provider.credentials,
        "Accept": "application/vnd.github.baptiste-preview+json"
    }

    url = os.path.join(git_provider.api_endpoint, relative_url)
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code < 400:
        repo = response.json()
        return Repository(
            owner=repo['owner']['login'], 
            name=repo['name'], 
            branch=repo['default_branch'], 
            git_provider=git_provider, 
            ssh_url=repo['ssh_url']
        )
    else:
        error = response.json()
        error_arr = [error.get('message')] + error.get('errors', [])
        raise RuntimeError("\n- ".join(error_arr))    
