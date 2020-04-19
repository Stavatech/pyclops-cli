from .django import django
from .react import react
from .clean import clean
from .aws import aws
from .docker import docker


cli_groups = [
    django,
    react,
    clean,
    aws,
    docker
]
