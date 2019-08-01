import click


@click.group()
def django():
    """Set up a Python Django application in the cloud"""


@click.command()
@click.option('--name', prompt='Stack name', help='The name that will be given to the stack')
@click.option('--domain', prompt='Web domain of service', help='The dmain that the service will be located at')
def create_stack(name, domain):
    """Simple program that greets NAME for a total of COUNT times."""
    # Steps:
    # 1) clone git repo
    # 2) create ECR repo
    # 3) publish docker image to ECR
    # 4) replace cfn placeholders
    # 5) create cfn service stack
    # 6) create cfn pipeline stack


django.add_command(create_stack)
