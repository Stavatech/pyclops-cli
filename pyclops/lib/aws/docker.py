import boto3


def create_repo(stack_name):
    client = boto3.client('ecr')
    
    response = client.create_repository(
        repositoryName='%s_repo' % stack_name,
        tags=[
            {
                'Key': 'product',
                'Value': 'stack_name'
            },
        ],
        imageTagMutability='IMMUTABLE'
    )

    return response['repository']
