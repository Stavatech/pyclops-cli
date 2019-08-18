import os
import requests
from pyclops.lib.git.github.template import Template
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository


def create_repo(git_provider:GithubProvider, owner:str, name:str, is_org:bool=False, optional_params:dict={}, template:Template=None) -> Repository:
    if template is not None:
        body = {"name": name, "owner": owner, **optional_params}  
        relative_url = "repos/%s/%s/generate" % (template.template_owner, template.template_repo)
    else:
        body = {"name": name, **optional_params}        
        if is_org:
            relative_url = "orgs/%s/repos" % owner
        else:
            relative_url = "%s/repos" % owner
    
    headers = {
        "Authorization": "token %s" % git_provider.credentials
    }

    url = os.path.join(git_provider.api_endpoint, relative_url)
    
    response = requests.post(url, json=body, headers=headers)
    repo = response.json()
    
    return Repository(owner=repo['owner']['login'], name=repo['name'], git_provider=git_provider, location=repo['html_url'])
