from pyclops.lib.git.provider import GitProvider
from pyclops.lib.io.process import run


class Repository(object):
    def __init__(self, git_provider:GitProvider, owner:str, name:str, location:str):
        self.owner = owner
        self.name = name
        self.git_provider = git_provider
        self.location = location
    
    def clone(self, local_dir:str="."):
        out, err, returncode = run("git clone %s.git" % self.location)
        if returncode != 0:
            print("stdout:\n", out, "stderr\n", err)
            raise RuntimeError("Failed to clone repository")
