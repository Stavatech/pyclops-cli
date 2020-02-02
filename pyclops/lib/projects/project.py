import os

from pyclops.lib.jinja import jinja
from pyclops.lib.git.repo import Repository
from pyclops.lib.io.build import clean


def generate_from_template(project_name:str, git_owner:str, is_org:bool, branch:str, template:Repository, params:dict, working_dir:str):
    """ Generates a new project from a Django template """   
    # Steps:    
    # 1) copy template repo
    template_dir = os.path.join(working_dir, "template")
    template.clone(local_dir=template_dir)

    new_repo = template.copy_to_new(owner=git_owner, new_repo_name=project_name, is_org=is_org)

    clean(path=template_dir)

    # 2) clone new repo
    new_repo.clone(local_dir=working_dir)

    # 3) run jinja preprocessor to set project_name
    jinja.process_dir(path=working_dir, params=params, in_place=True, suffix=".pyclops", remove_suffix=True)

    # 3) push the processed repo to remote
    new_repo.add(path=".")
    new_repo.commit(commit_message="Generated project according to parameters")
    new_repo.push()

    print("\nGenerated repository: %s" % new_repo.html_url)
    