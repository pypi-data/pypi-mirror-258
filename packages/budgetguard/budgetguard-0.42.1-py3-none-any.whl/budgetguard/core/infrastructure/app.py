import os
from aws_cdk import App
from aws_cdk import Environment
from cdk_infrastructure.lambdas.raw_to_bronze_stack import (
    RawToBronzeLambdaStack,
)
from cdk_infrastructure.lambdas.constants import RAW_TO_BRONZE_TABLE_NAMES
from cdk_infrastructure.lambdas.ingestion_stack import IngestionLambdaStack
from cdk_infrastructure.lambdas.master_exchange_rates_stack import (
    ExchangeRatesLambdaStack,
)
from cdk_infrastructure.s3_buckets.stack import S3DeployStack
from cdk_infrastructure.glue.stack import (
    GlueDataCatalogStack,
    GlueCrawlersStack,
)
from cdk_infrastructure.s3_buckets.constants import BUCKET_NAMES
from cdk_infrastructure.ecr.budget_guard_ecr_stack import (
    BudgetGuardECRStack,
    BudgetGuardEMRECRStack,
)
from dotenv import load_dotenv

load_dotenv()

env = Environment(
    account=os.environ.get("AWS_ACCOUNT_ID"),
    region=os.environ.get("AWS_REGION_NAME"),
)

app = App()

# Create Lambdas
IngestionLambdaStack(
    app, "LambdaIngestionStack", image_name="budget-guard", env=env
)

for table_name in RAW_TO_BRONZE_TABLE_NAMES:
    RawToBronzeLambdaStack(
        app,
        f"RawToBronzeLambda{table_name.title()}Stack",
        table_name=table_name,
        image_name="budget-guard",
        env=env,
    )

ExchangeRatesLambdaStack(
    app,
    "ExchangeRatesLambdaStack",
    image_name="budget-guard",
    env=env,
)

# Create buckets
for bucket_name in BUCKET_NAMES:
    S3DeployStack(app, f"{bucket_name}Stack", bucket_id=bucket_name, env=env)

S3DeployStack(
    app,
    "BudgetGuardMainCodeStack",
    bucket_id="budget-guard-main",
    env=env,
)

S3DeployStack(
    app,
    "BudgetGuardMasterCodeStack",
    bucket_id="budget-guard-master",
    env=env,
)

# Create AWS Glue Data Catalog
GlueDataCatalogStack(app, "GlueDataCatalogStack", env=env)

# Create AWS Glue Crawlers
GlueCrawlersStack(
    app,
    "GlueCrawlersStack",
    env=env,
)

# Create ECR
BudgetGuardECRStack(app, "BudgetGuardECRStack", env=env)
BudgetGuardEMRECRStack(app, "BudgetGuardEMRECRStack", env=env)

app.synth()
