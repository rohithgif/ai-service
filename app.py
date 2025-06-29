import os
import aws_cdk as cdk

from ai_service.ai_service_stack import AiServiceStack
from ai_service.cdk_stack.api_gateway_stack import ApiGatewayStack
from ai_service.cdk_stack.bedrock_service_stack import BedrockServiceStack
from ai_service.cdk_stack.payment_service_provider_stack import PaymentServiceProviderStack

app = cdk.App()
env = cdk.Environment(account="453763909251", region="eu-north-1")

service_a_stack = BedrockServiceStack(app, "BedrockServiceStack", env=env)
service_b_stack = PaymentServiceProviderStack(app, "PaymentServiceProviderStack", env=env)

ApiGatewayStack(
    app, 
    "ApiGatewayStack",
    env=env,
    service_a_fn=service_a_stack.lambda_function,
    service_b_fn=service_b_stack.lambda_function
)

app.synth()
