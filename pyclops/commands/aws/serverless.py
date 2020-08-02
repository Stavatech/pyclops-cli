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
from pyclops.lib.io.context_managers import cd
from pyclops.lib.io import build as build_utils
from pyclops.lib.projects.params import load_params
from pyclops.lib.projects.project import extract_project_params, generate_from_template


BUILD_DIR = os.path.join(
    build_utils.BUILD_DIR,
    'serverless'
)

DEFAULT_PROVIDER = "github"
DEFAULT_TEMPLATE = "Stavatech/AWS-Serverless-Template"

git_providers = {
    "github": GithubProvider() 
}


@click.group()
def serverless():
    """ Generate and build AWS Serverless projects """


@click.command()
@click.option('--project-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--provider', default=DEFAULT_PROVIDER, help='The git provider of the template repository')
@click.option('--template-repo', default=DEFAULT_TEMPLATE, help='The template git repository')
@click.option('--template-params', default=None, help='Comma-separated parameters required by the specific template being used e.g. param_1=abc,param_2=def')
@click.option('--destination-repo-owner', default=None, help='The git user or organization who will own the new repository (if this parameter is not supplied, creation of the remote git repository will be skipped)')
@click.option('--deployment-bucket', prompt="S3 deployment bucket", help='The bucket the deployment artifacts will be sent to when deploying to Lambda')
@click.argument('working-dir', type=click.Path())
def generate_project(project_name:str, provider:str, template_repo:str, template_params:str, destination_repo_owner:str, deployment_bucket:str, working_dir:str):
    """ Generates a new project from an AWS Serverless template """    
    git_provider = git_providers[provider]
    template = git_provider.get_repo(template_repo)

    params, destination_repo_params = extract_project_params(git_provider, project_name, template_params, destination_repo_owner)

    generate_from_template(template, params, destination_repo_params, working_dir)


@click.command()
@click.option('--templates-dir', default='./cfn/service', help='Directory containing template yml/jinja files')
@click.option('--app-dir', default='./app/', help='The directory that')
@click.option('--params-file', default='./params.py', help='Python file containing template parameters')
@click.option('--stage', default=None, help='The stage that the CloudFormation template is being generated for (if applicable)')
@click.option('--output-prefix', default='serverless', help='Prefix for the generated template and config files')
def package(templates_dir, app_dir, params_file, stage, output_prefix):
    """ Package and upload a serverless app to S3 and build a the CloudFormation template required to deploy it """
    build_utils.clean()
    os.makedirs(BUILD_DIR, exist_ok=True)

    params = load_params('params', params_file, stage)

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
