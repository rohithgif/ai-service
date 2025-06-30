from aws_cdk import Stack, aws_apigateway as apigw, aws_lambda as _lambda
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 service_a_fn: _lambda.IFunction,
                 service_b_fn: _lambda.IFunction,
                 service_c_fn: _lambda.IFunction,
                 service_index_fn: _lambda.IFunction,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        api = apigw.RestApi(self, "AI Service API",
                            rest_api_name="Services API",
                            description="API Gateway for Bedrock Service and Payment Service Provider")

        bedrock_res = api.root.add_resource("bedrock")
        bedrock_res.add_method("GET", apigw.LambdaIntegration(service_a_fn))

        payment_service_provider_res = api.root.add_resource("payment-service-provider")
        payment_service_provider_res.add_method("GET", apigw.LambdaIntegration(service_b_fn))

        exception_answering_ai_res = api.root.add_resource("exception-answering-ai")
        exception_answering_ai_res.add_method("POST", apigw.LambdaIntegration(service_c_fn))

        index_res = api.root.add_resource("build-index")
        index_res.add_method("POST", apigw.LambdaIntegration(service_index_fn))