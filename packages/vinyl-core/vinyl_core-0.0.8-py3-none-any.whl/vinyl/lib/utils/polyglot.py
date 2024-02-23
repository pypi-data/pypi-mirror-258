from typing import Any, Union

from sqlglot import dialects, exp, maybe_parse
from sqlglot._typing import E
from sqlglot.expressions import Expression, Identifier


def transform(ast_: Expression, transform_func: Any):
    # handles typing issues associated with null expressions
    if ast_ is None:
        pass
    else:
        ast_.transform(transform_func, copy=False)


def unquote_table_identifier(node: E) -> Union[E, Identifier]:
    if isinstance(node, exp.Identifier) and isinstance(node.parent, exp.Table):
        return exp.Identifier(this=node.name, quoted=False)
    return node


def unquote_tables(sql: str):
    ast: Expression = maybe_parse(sql, dialect=dialects.BigQuery)
    transform(ast, unquote_table_identifier)
    return ast.sql(dialect=dialects.BigQuery)
