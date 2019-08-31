import os

from pyclops.lib.git.provider import GitProvider
from pyclops.lib.io.process import run


class Repository(object):
    def __init__(self, git_provider:GitProvider, owner:str, name:str, branch:str, ssh_url:str):
        self.git_provider = git_provider
        self.owner = owner
        self.name = name
        self.branch = branch
        self.ssh_url = ssh_url
    
    def clone(self, local_dir:str="."):
        self.local_dir = local_dir
        out, err, returncode = run("git clone %s %s" % (self.ssh_url, self.local_dir))
        if returncode != 0:
            print("stdout:\n", out, "stderr\n", err)
            raise RuntimeError("Failed to clone repository")
    
    def add(self, path="."):
        os.chdir(self.local_dir)
        out, err, returncode = run("git add %s" % path)
        if returncode != 0:
            print("stdout:\n", out, "stderr\n", err)
            raise RuntimeError("Failed to stage changes")
    
    def commit(self, commit_message):
        os.chdir(self.local_dir)
        out, err, returncode = run("git commit -m '%s'" % commit_message)
        if returncode != 0:
            print("stdout:\n", out, "stderr\n", err)
            raise RuntimeError("Failed to commit changes")
    
    def push(self, remote="origin"):
        os.chdir(self.local_dir)
        out, err, returncode = run("git push %s %s" % (remote, self.branch))
        if returncode != 0:
            print("stdout:\n", out, "stderr\n", err)
            raise RuntimeError("Failed to push changes to remote")
