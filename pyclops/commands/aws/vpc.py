import os
import click

from pyclops.lib.git.github.provider import GithubProvider
from pyclops.lib.git.repo import Repository

from pyclops.lib.aws.cloudformation import build_cfn, get_stack, create_stack, update_stack
from pyclops.lib.projects.params import load_params


DEFAULT_VPC_TEMPLATE = Repository(GithubProvider(), 'Stavatech', 'VPC-Template', 'master', 'git@github.com:Stavatech/VPC-Template.git', 'https://github.com/Stavatech/VPC-Template.git')


def generate_subnet(az_index, cidr_index, is_public):
    name = "Public" if is_public else "Private"
    return {
        'name': '%sSubnet%s' % (name, str(az_index + 1)),
        'az_index': az_index,
        'cidr_block': '10.0.%s.0/24' % str(cidr_index),
        'is_public': is_public
    }


def write_params(params, path):
    with open(os.path.join(path, 'params.py'), 'w') as params_file:
        print('vpc_name = "%s"' % params['cidr_block'], file=params_file)
        print('cidr_block = "%s"' % params['cidr_block'], file=params_file)
        print('has_public_route = %s' % params['has_public_route'], file=params_file)
        print('has_private_route = %s' % params['has_private_route'], file=params_file)
        print('has_nat_gateway = %s' % params['has_nat_gateway'], file=params_file)
        print('subnets = %s' % params['subnets'], file=params_file)


@click.group()
def vpc():
    """ Pyclops operations for AWS VPC """


@click.command()
@click.option('--vpc-name', prompt='Project name', help='The name that will be used for the new repo and project')
@click.option('--num-AZs', default=1, help='The number of availability zones that subnets will be created in (for high availability)')
@click.option('--without-private-subnet', is_flag=True, help='Indicates whether private subnets be should be created in each availability zone')
@click.option('--without-public-subnet', is_flag=True, help='Indicates whether public subnets should be created in each availability zone')
@click.option('--with-nat-gateway', is_flag=True, help='Indicates whether a NAT gateway should be created in each availability zone')
@click.option('--git-owner', prompt="Git username/organisation", help='The git username or organisation (see --is-org) that will own the new repository')
@click.option('--is-org', is_flag=True, help='Indicates whether the git owner is a user or organisation')
def generate_repo(vpc_name, num_azs, without_private_subnet, without_public_subnet, with_nat_gateway, git_owner, is_org):
    """ Generates a VPC Pyclops repository from a template repository """
    private_subnet = without_private_subnet == False
    public_subnet = without_public_subnet == False

    # Steps:
    # 1) set up build directory
    build_dir = os.path.join(os.getenv('BUILD_DIR', './build'), 'aws/vpc')
    os.makedirs(build_dir, exist_ok=True)
    
    # 2) clone template repo
    repo_dir = os.path.join(build_dir, 'repo')
    repo = DEFAULT_VPC_TEMPLATE
    repo.clone(local_dir=repo_dir)

    # 3) generate params file
    subnets = []
    cidr_index = 0
    for az_index in range(num_azs):
        if not without_private_subnet:
            cidr_index = cidr_index + 1
            subnets.append(generate_subnet(az_index, cidr_index, False))
        if not without_public_subnet:
            cidr_index = cidr_index + 1
            subnets.append(generate_subnet(az_index, cidr_index, True))

    params = {
        'vpc_name': vpc_name,
        'cidr_block': '10.0.0.0/16',
        'has_public_route': not without_public_subnet,
        'has_private_route': not without_private_subnet,
        'has_nat_gateway': with_nat_gateway,
        'subnets': subnets
    }

    write_params(params, repo_dir)

    # 4) push the processed repo to a new remote
    repo.add(path=".")
    repo.commit(commit_message="Generated initial params.py file")
    new_repo = repo.copy_to_new(owner=git_owner, new_repo_name=vpc_name, is_org=is_org)

    print("Created new VPC repository: %s" % new_repo.html_url)


@click.command()
def build():
    build_dir = './build/aws/vpc/cfn'
    os.makedirs(build_dir, exist_ok=True)

    cfn_dir = "./cfn/"
    params_file = "./params.py"

    params = load_params('params', params_file)
    build_cfn(cfn_dir, params, build_dir=build_dir, output_prefix="vpc")


@click.command()
@click.option('--stack-name', prompt='Stack name', help='The name that will be given to the Cfn stack')
def deploy(stack_name):
    template_path = './build/aws/vpc/cfn/vpc.template.yml'
    with open(template_path, 'r') as template_file:
        template_body = template_file.read()

    if get_stack(stack_name):
        print("Stack already exists. Updating...")
        response = update_stack(stack_name, template_body, ['CAPABILITY_IAM'])
    else:
        print("Stack doesn't exist. Creating new stack...")
        response = create_stack(stack_name, template_body, ['CAPABILITY_IAM'])

    print("StackId: %s" % response['StackId'])


vpc.add_command(generate_repo)
vpc.add_command(build)
vpc.add_command(deploy)
