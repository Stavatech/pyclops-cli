import boto3
from botocore.exceptions import ClientError

from pyclops.lib.jinja import jinja


def build_cfn(templates_dir, params, build_dir, output_prefix="template"):
    """ Build a complete CloudFormation template from multiple source YAML and Jinja files """
    jinja.process_dir(templates_dir, params, build_dir=build_dir)


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
