import os
import requests

from pyclops.lib.git.repo import Repository


class GithubProvider(object):
    def __init__(self, credentials=os.getenv('GITHUB_OAUTH')):
        self.api_endpoint = 'https://api.github.com'
        self.credentials = credentials
    
    def create_repo(self, owner:str, name:str, is_org:bool=False, optional_params:dict={}) -> Repository:
        body = {"name": name, **optional_params}        
        if is_org:
            relative_url = "orgs/%s/repos" % owner
        else:
            relative_url = "user/repos"
        
        headers = {
            "Authorization": "token %s" % self.credentials
        }

        url = os.path.join(self.api_endpoint, relative_url)
        
        response = requests.post(url, json=body, headers=headers)
        if response.status_code < 400:
            repo = response.json()
            return Repository(
                owner=repo['owner']['login'], 
                name=repo['name'], 
                branch=repo['default_branch'], 
                git_provider=self, 
                ssh_url=repo['ssh_url'],
                html_url=repo['html_url']
            )
        else:
            error = response.json()
            print(error)
            error_arr = [error.get('message')] + error.get('errors', [])
            raise RuntimeError("\n- ".join(error_arr))  
