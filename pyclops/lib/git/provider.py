class GitProvider(object):
    def __init__(self):
        self.api_endpoint:str = None
        self.credentials:str = None

    def create_repo(self, *args, **kwargs):
        raise NotImplementedError()
