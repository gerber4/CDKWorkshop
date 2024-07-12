from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from cdk_dynamo_table_view import TableViewer

from .hitcounter import HitCounter

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello = _lambda.Function(
            self, "hello",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler"
        )

        hello_with_counter = HitCounter(
            self, "HelloWithHitCounter",
            downstream=hello
        )

        gateway = apigw.LambdaRestApi(
            self, "gateway",
            handler=hello_with_counter._handler
        )

        table_viewer = TableViewer(
            self, "TableViewer",
            title="Table Viewer",
            table=hello_with_counter._table
        )
