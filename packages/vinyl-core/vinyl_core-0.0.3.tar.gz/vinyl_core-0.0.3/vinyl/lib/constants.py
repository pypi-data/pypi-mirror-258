from typing import Literal

TS_COL_NAME = "ts"
METRIC_LABEL = "metric"
DIMENSION_LABEL = "dimension"
SCHEMA_LABEL = "schema"


class PreviewHelper:
    preview: Literal["full", "twin"] = "full"
