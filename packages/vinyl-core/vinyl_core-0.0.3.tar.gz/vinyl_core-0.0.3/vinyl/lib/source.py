import os
from typing import Any, Callable

import ibis
from ibis.common.exceptions import IbisError

from vinyl.lib.connect import DatabaseFileConnector, _DatabaseConnector, _TableConnector
from vinyl.lib.constants import PreviewHelper
from vinyl.lib.field import Field
from vinyl.lib.project import load_project_module
from vinyl.lib.table import VinylTable


def _get_twin_relative_path(name: str, *subdirs) -> str:
    return os.path.join(
        "data",
        *subdirs,
        f"{name}.duckdb",
    )


def source(resource: Callable[..., Any], sample_row_count: int = 1000):
    def decorator(cls) -> VinylTable:
        connector = resource()

        schema = []
        for name, attr in cls.__annotations__.items():
            schema.append((name, attr))

        ibis.table(schema, name=cls._unique_name)
        table = VinylTable.create_from_schema(
            ibis.Schema.from_tuples(schema), cls._unique_name
        )
        parent_name = ".".join(cls.__module__.split(".")[2:])

        for name, attr in cls.__annotations__.items():
            field = Field(
                name=name, type=attr, parent_table=table, parent_name=parent_name
            )
            if hasattr(cls, name):
                current = getattr(cls, name)
                # Field info overrides the class level attributes, may want to change
                field.update(**current.asdict())
            setattr(cls, name, field)

        table = VinylTable.create_from_schema(
            ibis.Schema.from_tuples(schema), cls._unique_name
        )

        table._is_vinyl_source = True  # helps find sources in the project for load_defs
        table._source_class = cls

        # update parent table to include the full set of annotations and save graph
        for name, attr in cls.__annotations__.items():
            current = getattr(cls, name)
            # Field info overrides the class level attributes, may want to change
            current.update(**{"parent_table": table})
            setattr(cls, name, current)
            current.store_relations()

        unbounded_op = table.tbl.op()
        if isinstance(connector, _DatabaseConnector):

            def full_connection():
                return connector.get_table(
                    database=cls._database, schema=cls._schema, table=cls._table
                ).op()

            if PreviewHelper.preview == "full":
                table._conn_replace = {unbounded_op: full_connection}
            elif PreviewHelper.preview == "twin":
                # get twin
                twin_conn = DatabaseFileConnector(
                    os.path.join(
                        os.path.dirname(load_project_module().__file__),
                        _get_twin_relative_path(resource.__name__),
                    )
                )

                try:
                    table._twin_conn_replace = {
                        unbounded_op: lambda: twin_conn.get_table(
                            database=twin_conn.database,
                            schema=cls._schema,
                            table=cls._table,
                        ).op()
                    }
                except IbisError:
                    # twin doesn't exist, fall back to full conn, but not connected yet
                    table._conn_replace = {unbounded_op: full_connection}

            else:
                raise ValueError(
                    f"Invalid value for PreviewHelper.preview: {PreviewHelper.preview}"
                )
        elif isinstance(connector, _TableConnector):

            def full_connection():
                # for file connectors, we reconnect to the individual file to get the correct table. Since these tables are not in memory, we need to read to get the location.
                adj_conn = type(connector)(cls._path)
                adj_conn.connect()
                tbl_for_op = next(iter(adj_conn.tbls.values()))
                return tbl_for_op.op()

            if PreviewHelper.preview == "full":
                table._conn_replace = {unbounded_op: full_connection}

            elif PreviewHelper.preview == "twin":
                try:
                    table._twin_conn_replace = {
                        unbounded_op: table.tbl.filter(
                            ibis.random()
                            < ibis.least(sample_row_count / cls._row_count, 1)
                        ).op()
                    }
                except IbisError:
                    # twin doesn't exist, fall back to full conn, but not connected yet
                    table._conn_replace = {unbounded_op: full_connection}
        else:
            raise NotImplementedError(
                f"Connector type {type(connector)} is not yet supported"
            )

        return table

    return decorator
