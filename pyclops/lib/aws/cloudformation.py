import os
import glob

import boto3
from botocore.exceptions import ClientError

from pyclops.lib.jinja import jinja
from pyclops.lib.yaml import yaml


def build_cfn(templates_dir, params, build_dir, output_prefix="cfn"):
    """ Build a complete CloudFormation template from multiple source YAML and Jinja files """
    jinja.process_dir(templates_dir, params, build_dir=build_dir)
    
    yaml_glob_path = os.path.join(build_dir, "*.template.yml")
    json_glob_path = os.path.join(build_dir, "*.template.json")

    yaml_templates = glob.glob(yaml_glob_path)
    json_templates = glob.glob(json_glob_path)

    templates = yaml_templates + json_templates

    merged_template = yaml.merge(templates)

    validate_cfn(merged_template)

    file_name = os.path.join(build_dir, output_prefix + ".template.yml")
    yaml_file = yaml.write_yaml_file(merged_template, file_name)

    print("Generated %s" % yaml_file)

    return yaml_file


def validate_cfn(template_dict):
    print("Validating CFN template...")
    
    valid_top_level_keys = [
        'AWSTemplateFormatVersion',
        'Outputs',
        'Parameters',
        'Conditions',
        'Resources',
        'Mappings'
    ]

    for key in template_dict.keys():
        if key not in valid_top_level_keys:
            raise Exception("CFN template contains invalid top-level key: %s" % key)


def get_stack(stack_name):
    client = boto3.client('cloudformation')
    try:
        return client.describe_stacks(StackName=stack_name)
    except ClientError as ce:
        return None


def create_stack(stack_name, template_body, capabilities=[]):
    client = boto3.client('cloudformation')
    return client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=capabilities
    )


def update_stack(stack_name, template_body, capabilities=[]):
    client = boto3.client('cloudformation')
    return client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=capabilities
    )
