import os

from pyclops.lib.git.provider import GitProvider
from pyclops.lib.io.process import run
from pyclops.lib.io.context_managers import cd


def _run_git_cmd(cmd:str, error_message:str):
    out, err, returncode = run(cmd)
    if returncode != 0:
        print("stdout:\n", out, "stderr\n", err)
        raise RuntimeError(error_message)


class Repository(object):
    def __init__(self, git_provider:GitProvider, owner:str, name:str, branch:str, ssh_url:str, html_url:str):
        self.git_provider = git_provider
        self.owner = owner
        self.name = name
        self.branch = branch
        self.ssh_url = ssh_url
        self.html_url = html_url
    
    def clone(self, local_dir:str="."):
        self.local_dir = local_dir
        _run_git_cmd("git clone %s %s" % (self.ssh_url, self.local_dir), "Failed to clone repository")
    
    def add(self, path:str="."):
        with cd(path=self.local_dir):
            _run_git_cmd("git add %s" % path, "Failed to stage changes")
    
    def commit(self, commit_message:str):
        with cd(path=self.local_dir):
            _run_git_cmd("git commit -m '%s'" % commit_message, "Failed to commit changes")
    
    def push(self, remote:str="origin"):
        with cd(path=self.local_dir):
            _run_git_cmd("git push %s %s" % (remote, self.branch), "Failed to push changes to remote")
    
    def copy_to_new(self, owner:str, new_repo_name:str, is_org:bool=False):
        with cd(path=self.local_dir):
            repo = self.git_provider.create_repo(owner=owner, name=new_repo_name, is_org=is_org)
            repo.local_dir = self.local_dir
            _run_git_cmd("git remote add copy %s" % repo.ssh_url, "Failed to add new remote")
            self.push(remote="copy")
            return repo
