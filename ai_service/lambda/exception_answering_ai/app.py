import boto3
import os

s3 = boto3.client('s3')

def handler(event, context):
    bucket_name = 'grabhackbucket'
    prefix = 'projects'

    paginator = s3.get_paginator('list_objects_v2')
    files = []

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if not key.endswith('/'):
                    files.append(key)
                    print(f"Found file: {key}")

    return {
        "statusCode": 200,
        "body": f"Found files: {files}"
    }
