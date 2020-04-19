import os
import glob
import json

import boto3
from botocore.exceptions import ClientError

from pyclops.lib.jinja import jinja
from pyclops.lib.yaml import yaml


def build_cfn(templates_dir, params, build_dir, output_prefix="cfn"):
    """ Build a complete CloudFormation template from multiple source YAML and Jinja files """
    jinja.process_dir(templates_dir, params, build_dir=build_dir)
    
    yml_glob_path = os.path.join(build_dir, "*.template.yml")
    yaml_glob_path = os.path.join(build_dir, "*.template.yaml")
    json_glob_path = os.path.join(build_dir, "*.template.json")

    yml_templates = glob.glob(yml_glob_path)
    yaml_templates = glob.glob(yaml_glob_path)
    json_templates = glob.glob(json_glob_path)

    templates = yml_templates + yaml_templates + json_templates

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
        'Mappings',
        'Transform',
        'Description',
        'Globals'
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


def create_stack(stack_name, template_body, capabilities=[], parameters=[]):
    client = boto3.client('cloudformation')
    return client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=capabilities,
        Parameters=parameters
    )


def update_stack(stack_name, template_body, capabilities=[], parameters=[]):
    client = boto3.client('cloudformation')
    return client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=capabilities,
        Parameters=parameters
    )

def extract_parameters_from_config(template_config):
    if not os.path.isfile(template_config):
        raise Exception('An invalid path was specified for the template config file: %s' % template_config)

    param_list = []
    with open(template_config, 'r') as config:
        params = json.loads(config.read()).get('Parameters')
        if params:
            param_list = [{key: value} for key, value in params.items()]

    return param_list

def transform_template_values(template_file, resource_type, resource_property, value):
    yaml_dict = yaml.read_yaml_file(template_file)

    for resource_name, resource in yaml_dict['Resources'].items():
        if resource['Type'] == resource_type:
            print('Resource "%s" matched type "%s". Transforming "%s" property from "%s" to "%s".' % (
                resource_name, 
                resource_type, 
                resource_property, 
                resource['Properties'][resource_property], 
                value
            ))
            resource['Properties'][resource_property] = value

    yaml.write_yaml_file(yaml_dict, template_file)
