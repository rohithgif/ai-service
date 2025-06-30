from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    Duration,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct

class ExceptionQueryAICdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(
            self, 
            "GrabHackBucket", 
            "grabhackbucket"
        )

        # Vector indexing Lambda
        vector_indexing_lambda = _lambda.DockerImageFunction(
            self, 
            "VectorIndexingFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="ai_service/lambda/s3_files_to_vector_index"
            ),
            timeout=Duration.minutes(15),
            memory_size=3000
        )

        # Query Lambda
        query_lambda = _lambda.DockerImageFunction(
            self, 
            "ExceptionQueryFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="ai_service/lambda/exception_answering_ai"
            ),
            timeout=Duration.minutes(15),
            memory_size=3000
        )

        # Grant S3 permissions to both functions
        bucket.grant_read_write(vector_indexing_lambda)
        bucket.grant_read_write(query_lambda)

        for lambda_fn in [vector_indexing_lambda, query_lambda]:
            lambda_fn.add_to_role_policy(iam.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn]
            ))

        # Grant Bedrock access to query Lambda
        query_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        self.vector_indexing_lambda = vector_indexing_lambda
        self.lambda_function = query_lambda