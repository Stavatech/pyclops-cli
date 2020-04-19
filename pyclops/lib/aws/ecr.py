import boto3
import base64


def create_repo(repo_name: str) -> str:
    """ Create an ECR repository and return the ARN """
    ecr = boto3.client('ecr')
    return ecr.create_repository(repositoryName=repo_name)['repository']['repositoryArn']


def get_authorization_data():
    ecr = boto3.client('ecr')
    token = ecr.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode("utf-8").split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']
    return username, password, registry


def get_repo(repo_name, registryId=None):
    ecr = boto3.client('ecr')

    params = {'repositoryNames': [repo_name]}
    if registryId:
        params['registryId'] = registryId
    
    repositories = ecr.describe_repositories(**params)['repositories']
    
    if len(repositories) == 1:
        return repositories[0]
    else:
        error_message = f"Respository '{repo_name}' not found" if len(repositories) == 0 \
            else f"More than one repository named '{repo_name}'"
        raise Exception(error_message)
