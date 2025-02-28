from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
)

class HitCounter(Construct):
    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, "Hits",
            partition_key={"name": "path", "type": ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, "HitCountHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambda"),
            handler="hitcounter.handler",
            environment={
                "HITS_TABLE_NAME": self._table.table_name,
                "DOWNSTREAM_FUNCTION_NAME": downstream.function_name
            }
        )

        self._table.grant_read_write_data(self._handler)
        downstream.grant_invoke(self._handler)
