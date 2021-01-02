import os
import sys
import requests

from pyclops.lib.git.repo import Repository


class GithubProvider(object):
    def __init__(self, credentials=os.getenv('GITHUB_TOKEN')):
        self.api_endpoint = 'https://api.github.com'
        self.credentials = credentials
    
    def create_repo(self, owner:str, name:str, is_org:bool=False, optional_params:dict={}) -> Repository:        
        if is_org:
            relative_url = f"orgs/{owner}/repos"
        else:
            relative_url = "user/repos"
        
        url = os.path.join(self.api_endpoint, relative_url)
        headers = self._get_auth_header()
        body = {"name": name, **optional_params}
        
        response = requests.post(url, json=body, headers=headers)
        return self._handle_repo_response(response)
        
    def get_repo(self, relative_location:str):
        url = f"{self.api_endpoint}/repos/{relative_location}"
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        return self._handle_repo_response(response)
        
    def get_user(self):
        url = f"{self.api_endpoint}/user"
        headers = self._get_auth_header()

        response = requests.get(url, headers=headers)

        if response.status_code >= 400:
            error = response.json()
            raise RuntimeError(error.get('message'))

        return response.json()['login']
        
    def is_org(self, git_namespace):
        url = f"{self.api_endpoint}/orgs/git_namespace"
        headers = self._get_auth_header()

        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            return False
        
        if response.status_code >= 400:
            error = response.json()
            raise RuntimeError(error.get('message'))

        return response.status_code == 200
    
    def _handle_repo_response(self, response) -> Repository:
        if response.status_code >= 400:
            error = response.json()
            raise RuntimeError(error.get('message'))  

        repo = response.json()
        return Repository(
            owner=repo['owner']['login'], 
            name=repo['name'], 
            branch=repo['default_branch'], 
            git_provider=self, 
            ssh_url=repo['ssh_url'],
            html_url=repo['html_url']
        )
    
    def _get_auth_header(self) -> dict:
        if not self.credentials:
            sys.stderr.write("Error: Github credntials not found. Has the GITHUB_TOKEN environment variable been set?\n")
            sys.exit(-1)
        
        return {
            "Authorization": "token %s" % self.credentials
        }
        
    