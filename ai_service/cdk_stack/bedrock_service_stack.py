from aws_cdk import Stack, aws_lambda as _lambda
from constructs import Construct

class BedrockServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.lambda_function = _lambda.Function(
            self, "BedrockServiceFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="app.handler",
            code=_lambda.Code.from_asset("ai_service/lambda/bedrock_service")
        )
