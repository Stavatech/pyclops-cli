import os


class GithubProvider(object):
    def __init__(self, credentials=os.getenv('GITHUB_OAUTH')):
        self.api_endpoint = 'https://api.github.com'
        self.credentials = credentials
