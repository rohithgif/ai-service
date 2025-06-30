import os
import aws_cdk as cdk

from ai_service.ai_service_stack import AiServiceStack
from ai_service.cdk_stack.api_gateway_stack import ApiGatewayStack
from ai_service.cdk_stack.bedrock_service_stack import BedrockServiceStack
from ai_service.cdk_stack.payment_service_provider_stack import PaymentServiceProviderStack
from ai_service.cdk_stack.s3_files_list_stack import S3ListFilesCdkStack

app = cdk.App()
env = cdk.Environment(account="453763909251", region="eu-north-1")

bedrock_service_stack = BedrockServiceStack(app, "BedrockServiceStack", env=env)
payment_service_provider_stack = PaymentServiceProviderStack(app, "PaymentServiceProviderStack", env=env)
exception_query_ai_stack = ExceptionQueryAICdkStack(app, "ExceptionQueryAICdkStack", env=env)
vector_index_stack = S3FilesToVectorIndexStack(app, "S3FilesToVectorIndexStack", env=env)

ApiGatewayStack(
    app, 
    "ApiGatewayStack",
    env=env,
    service_a_fn=bedrock_service_stack.lambda_function,
    service_b_fn=payment_service_provider_stack.lambda_function,
    service_c_fn=exception_query_ai_stack.lambda_function,
    service_index_fn=vector_index_stack.lambda_function
)

app.synth()
