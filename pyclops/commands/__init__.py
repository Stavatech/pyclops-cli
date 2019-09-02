from .django import django
from .react import react
from .cloudformation import cloudformation
from .aws import aws


cli_groups = [
    django,
    react,
    cloudformation,
    aws
]
