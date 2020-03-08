import os
import sys
import boto3
import botocore


def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    params = {'Bucket': bucket_name}

    if s3.meta.region_name != "us-east-1":
        params['CreateBucketConfiguration'] = {'LocationConstraint': s3.meta.region_name}
        
    try:
        s3.create_bucket(**params)
    except botocore.exceptions.ClientError as e:
        print(e)
        if not e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
            sys.exit(1)


def write_file(bucket_name, file_path):
    s3 = boto3.resource('s3')

    s3_object = s3.Object(bucket_name, os.path.basename(file_path))
    s3_object.put(Body=open(file_path, 'rb'))

    return f"s3://{s3_object.bucket_name}/{s3_object.key}"
