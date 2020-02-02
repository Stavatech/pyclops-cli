import os
import sys
import click
import zipfile
import glob
import secrets
import string

from pyclops.lib.jinja import jinja
from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository
from pyclops.lib.aws.cloudformation import (
    build_cfn,
    get_stack,
    create_stack,
    update_stack,
    transform_template_values
)
from pyclops.lib.aws.s3 import create_bucket, write_file
from pyclops.lib.io.params import load_params
from pyclops.lib.io.context_managers import cd
from pyclops.lib.io import build as build_utils


BUILD_DIR = os.path.join(
    build_utils.BUILD_DIR,
    'serverless'
)

DEFAULT_SERVERLESS_TEMPLATE = Repository(
    GithubProvider(), 
    'Stavatech', 
    'AWS-Serverless-Template', 
    'master', 
    'git@github.com:Stavatech/AWS-Serverless-Template', 
    'https://github.com/Stavatech/AWS-Serverless-Template-Template.git'
)


@click.group()
def serverless():
    """ Pyclops operations for AWS VPC """


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--git-owner', prompt="Git username/organisation", help='The git username or organisation (see --is-org) that will own the new repository')
@click.option('--is-org', is_flag=True, help='Indicates whether the git owner is a user or organisation')
@click.option('--branch', default='master', help='The branch that monitored during deployments')
@click.option('--template', default=DEFAULT_SERVERLESS_TEMPLATE, help='The template git repository')
@click.option('--deployment-bucket', prompt="S3 deployment bucket", help='The bucket the deployment artifacts will be sent to when deploying to Lambda')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name:str, git_owner:str, is_org:bool, branch:str, template:Repository, deployment_bucket:str, working_dir:str):
    """ Generates a new project from an AWS Serverless template """   
    # Steps:     
    # 1) copy template repo
    template_dir = os.path.join(working_dir, "template")
    template.clone(local_dir=template_dir)

    new_repo = template.copy_to_new(owner=git_owner, new_repo_name=project_name, is_org=is_org)

    build_utils.clean(path=template_dir)

    # 2) clone new repo
    new_repo.clone(local_dir=working_dir)

    # 3) run jinja preprocessor to set project_name
    params = {
        'project_name': project_name,
        'git_owner': git_owner,
        'git_branch': branch,
        's3_deployment_bucket': deployment_bucket
    }
    jinja.process_dir(path=working_dir, params=params, in_place=True, suffix=".pyclops", remove_suffix=True)

    # 3) push the processed repo to remote
    new_repo.add(path=".")
    new_repo.commit(commit_message="Generated project according to parameters")
    new_repo.push()

    print("\nGenerated repository: %s" % new_repo.html_url)


@click.command()
@click.option('--templates-dir', default='./cfn/service', help='Directory containing template yml/jinja files')
@click.option('--app-dir', default='./app/', help='The directory that')
@click.option('--params-file', default='./params.py', help='Python file containing template parameters')
@click.option('--stage', default=None, help='The stage that the CloudFormation template is being generated for (if applicable)')
@click.option('--output-prefix', default='serverless', help='Prefix for the generated template and config files')
def package(templates_dir, app_dir, params_file, stage, output_prefix):
    """ Build a complete CloudFormation template from multiple source YAML and Jinja files """
    build_utils.clean()
    os.makedirs(BUILD_DIR, exist_ok=True)

    params = load_params('params', params_file)

    s3_deployment_bucket = params['s3_deployment_bucket']
    create_bucket(s3_deployment_bucket)

    package_name = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
    package_path = '%s/%s' % (BUILD_DIR, package_name)

    with zipfile.ZipFile(package_path, 'w') as package:
        with cd(app_dir):
            files = glob.glob('*/**', recursive=True)
            for filepath in files:
                package.write(filepath)
    
    print("Writing packaged app to S3...")
    s3_path = write_file(s3_deployment_bucket, package_path)

    yaml_file = build_cfn(templates_dir, params, build_dir=BUILD_DIR, output_prefix=output_prefix)
    transform_template_values(yaml_file, 'AWS::Serverless::Function', 'CodeUri', s3_path)


serverless.add_command(generate_project)
serverless.add_command(package)
