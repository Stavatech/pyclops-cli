import boto3


def create_repo(repo_name: str) -> str:
    """ Create an ECR repository and return the ARN """
    ecr = boto3.client('ecr')
    return ecr.create_repository(repositoryName=repo_name)['repository']['repositoryArn']