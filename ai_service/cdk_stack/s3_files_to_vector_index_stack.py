from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class S3FilesToVectorIndexStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Reference existing bucket
        bucket = s3.Bucket.from_bucket_name(
            self,
            "GrabHackBucket",
            "grabhackbucket"
        )

        # Lambda for building vector index
        docker_asset = ecr_assets.DockerImageAsset(
            self,
            "S3FilesToVectorIndexImage",
            directory="ai_service/lambda/s3_files_to_vector_index"
        )

        index_lambda = _lambda.DockerImageFunction(
            self,
            "S3FilesToVectorIndexFunction",
            code=_lambda.DockerImageCode.from_image_asset(docker_asset.image_uri),
            timeout=Duration.minutes(15),
            memory_size=3000
        )

        # Grant permissions
        for fn in [index_lambda]:
            bucket.grant_read_write(fn)
            fn.add_to_role_policy(iam.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn]
            ))
            fn.add_to_role_policy(iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=["*"]  # Ideally narrow to your Bedrock model ARN
            ))

        # Expose Lambdas
        self.lambda_function =index_lambda
