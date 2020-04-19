import os
import click
import json

from pyclops.lib.projects.params import load_params
from pyclops.lib.aws.cloudformation import (
    build_cfn,
    get_stack,
    create_stack,
    update_stack,
    extract_parameters_from_config
)
from pyclops.lib.io import build as build_utils


BUILD_DIR = os.path.join(
    build_utils.BUILD_DIR,
    'cfn'
)


@click.group()
def cloudformation():
    """ Build and deploy CloudFormation stacks """


@click.command()
@click.option('--templates-dir', prompt='Templates directory', help='Directory containing template yml/jinja files')
@click.option('--params-file', prompt='Parameter file', help='Python file containing template parameters')
@click.option('--stage', default=None, help='The stage that the CloudFormation template is being generated for (if applicable)')
@click.option('--output-prefix', default='cfn', help='Prefix for the generated template and config files')
def build(templates_dir, params_file, stage, output_prefix):
    """ Build a complete CloudFormation template from multiple source YAML and Jinja files """
    build_utils.clean(BUILD_DIR)
    params = load_params('params', params_file, stage)
    build_cfn(templates_dir, params, build_dir=BUILD_DIR, output_prefix=output_prefix)


@click.command()
@click.option('--stack-name', prompt='Stack name', help='CloudFormation stack name')
@click.option('--template-file', prompt='Template file', help='CloudFormation template file (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html#w2ab1c13c15c13)')
@click.option('--template-config', default=None, help='CloudFormation template config file (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html#w2ab1c13c15c15)')
@click.option('--parameter-overrides', default=None, help='Parameter overrides in the format: ParamName1=ParamValue1,ParamName2=ParamValue2')
@click.option('--capabilities', default='CAPABILITY_IAM', help='Comma-separated list of CFN IAM capabilities')
def deploy(stack_name, template_file, template_config, parameter_overrides, capabilities):
    """ Deploy a CloudFormation template to AWS """
    with open(template_file, 'r') as template:
        template_body = template.read()
    
    params = []

    if template_config:
        params = extract_parameters_from_config(template_config)

    if parameter_overrides:
        for parameter_override in parameter_overrides.split(','):
            key, value = tuple(parameter_override.split('='))
            params[key] = value
    
    formatted_params = [{
        'ParameterKey': list(param.keys())[0],
        'ParameterValue': list(param.values())[0]
    } for param in params]

    if get_stack(stack_name):
        print("Stack already exists. Updating...")
        response = update_stack(stack_name, template_body, capabilities.split(','), formatted_params)
    else:
        print("Stack doesn't exist. Creating new stack...")
        response = create_stack(stack_name, template_body, capabilities.split(','), formatted_params)

    print("StackId: %s" % response['StackId'])


cloudformation.add_command(build)
cloudformation.add_command(deploy)