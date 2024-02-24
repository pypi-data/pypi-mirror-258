from aws_cdk import Stack, Aws, Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ecr as _ecr
from aws_cdk import aws_iam as _iam
from constructs import Construct


class ExchangeRatesLambdaStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, image_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.build_lambda_func(self.get_lambda_image(image_name))

    def get_lambda_image(self, image_name: str):
        ecr_repository = _ecr.Repository.from_repository_attributes(
            self,
            id="ECR",
            repository_arn="arn:aws:ecr:{0}:{1}:repository".format(
                Aws.REGION, Aws.ACCOUNT_ID
            ),
            repository_name=image_name,
        )
        ecr_image = _lambda.DockerImageCode.from_ecr(
            repository=ecr_repository,
            tag_or_digest="latest",
            cmd=[
                "budgetguard.core.lambda_functions.master_exchange_rates.lambda_handler"  # noqa
            ],
            entrypoint=["python", "-m", "awslambdaric"],
        )
        return ecr_image

    def build_lambda_func(self, lambda_image: _lambda.Code):
        exchange_rates_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="ExchangeRatesLambda",
            function_name="ExchangeRatesLambda",
            code=lambda_image,
            timeout=Duration.seconds(300),
            memory_size=1024,
        )
        exchange_rates_lambda.add_to_role_policy(
            _iam.PolicyStatement(
                actions=["s3:GetObject", "s3:PutObject"],
                resources=["arn:aws:s3:::budget-guard-master/*"],
                effect=_iam.Effect.ALLOW,
            )
        )

        exchange_rates_lambda.add_to_role_policy(
            _iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=[
                    f"arn:aws:secretsmanager:us-east-1:{Aws.ACCOUNT_ID}:secret:budget_guard_nordigen_key-OCfS6T"  # noqa
                ],
                effect=_iam.Effect.ALLOW,
            )
        )
