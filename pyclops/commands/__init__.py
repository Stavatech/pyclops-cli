from .django import django
from .react import react
from .cloudformation import cloudformation
from .clean import clean
from .aws import aws


cli_groups = [
    django,
    react,
    cloudformation,
    clean,
    aws
]
