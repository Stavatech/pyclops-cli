import os
import click

from pyclops.lib.io.modules import load_params
from pyclops.lib.aws.cloudformation import build_cfn
from pyclops.lib.io import build as build_utils


BUILD_DIR = os.path.join(
    os.getenv('BUILD_DIR', './build'),
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

    params = load_params('params', params_file)

    if stage:
        params['stage'] = stage
        stage_params = params['stages'][stage]
        for key in stage_params.keys():
            params['stage_%s' % key] = stage_params[key]

    build_cfn(templates_dir, params, build_dir=BUILD_DIR, output_prefix=output_prefix)


@click.command()
@click.option('--stack-name', prompt='Stack name', help='CloudFormation stack name')
@click.option('--template-file', prompt='Template file', help='CloudFormation template file (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html#w2ab1c13c15c13)')
@click.option('--template-config', prompt='Template config file', help='CloudFormation template config file (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html#w2ab1c13c15c15)')
@click.option('--parameter-overrides', prompt='Template parameter overrides', help='Parameter overrides in the format: ParamName1=ParamValue1,ParamName2=ParamValue2')
def deploy(stack_name, template_file, template_config, parameter_overrides):
    """ Deploy a CloudFormation template to AWS """
    pass


cloudformation.add_command(build)
cloudformation.add_command(deploy)