from .aws import aws
from .clean import clean
from .docker import docker
from .templates import templates


cli_groups = [
    aws,
    clean,
    docker,
    templates
]
