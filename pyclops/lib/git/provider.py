class GitProvider(object):
    def __init__(self):
        self.api_endpoint:str = None
        self.credentials:str = None

    def create_repo(self, *args, **kwargs):
        raise NotImplementedError()

    def get_repo(self, relative_location:str):
        raise NotImplementedError()

    def get_user(self):
        raise NotImplementedError()

    def is_org(self, git_namespace:str):
        raise NotImplementedError()
