from __future__ import annotations

import json
import os
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import ibis
import ibis.expr.types as ir
from ibis import Schema
from ibis.backends.base import BaseBackend
from tqdm import tqdm

from vinyl.lib.utils.pkg import get_project_directory
from vinyl.lib.utils.text import extract_uri_scheme

TEMP_PATH_PREFIX = "vinyl_"


class DataTable:
    name: str
    resource: _ResourceConnector
    path: str | None
    database: str | None
    schema: str | None
    table: str | None

    def __init__(
        self,
        table: str,
        resource: _ResourceConnector,
        path: str | None = None,
        database: str | None = None,
        schema: str | None = None,
    ):
        self.table = table
        self.resource = resource
        self.path = path
        self.database = database
        self.schema = schema

    def get_table(self):
        if (
            self.path is not None
            and self.database is None
            and self.schema is None
            and self.table is None
        ):
            return self.resource.get_table(self.path)
        return self.resource.get_table(self.database, self.schema, self.table)


@dataclass
class Source:
    name: str
    location: str
    schema: Schema | None
    parent_resource: Any | None = None


class _ResourceConnector(ABC):
    """Base interface for handling connecting to resource and getting sources"""

    @abstractmethod
    def list_sources(self, with_schema=False) -> list[Source]:
        pass

    @abstractmethod
    def connect(self) -> BaseBackend:
        pass


# exists to help distinguish between table and database connectors
class _TableConnector(_ResourceConnector):
    tbls: dict[str, ir.Table]

    def __init__(self, path: str):
        self.path = path

    def get_table(self, path):
        # for file connectors, we reconnect to the individual file to get the correct table. Since these tables are not in memory, we need to read to get the location.
        adj_conn = self.__class__(path)
        adj_conn.connect()
        return next(iter(adj_conn.tbls.values()))

    def generate_twin(self, path, sample_row_count=1000):
        tbl = self.get_table(path)
        row_count = tbl.count()
        sampled = tbl.filter(
            ibis.random() < ibis.least(sample_row_count / row_count, 1)
        )
        return sampled


class _DatabaseConnector(_ResourceConnector):
    conn: ibis.backends.base.BaseBackend
    allows_multiple_databases: bool = True
    tables: list[str]
    excluded_dbs: list[str] = []
    excluded_schemas: list[str] = []

    def find_sources_in_db(
        self,
        databases_override: list[str] | None = None,
        with_schema=False,
    ):
        self.connect()

        sources = []
        preprocess = []

        # get tables
        for loc in self.tables:
            database, schema, table = loc.split(".")
            if databases_override is not None:
                adj_databases = databases_override
            elif database == "*":
                if not hasattr(self.conn, "list_databases"):
                    raise ValueError(
                        f"Database specification required for this connector: {self.__class__.__name__}"
                    )
                adj_databases = list(
                    set(self.conn.list_databases()) - set(self.excluded_dbs)
                )
            else:
                adj_databases = [database]

            for db in adj_databases:
                if schema == "*":
                    schema_set = set(
                        self.conn.list_schemas(database=db)
                        if self.allows_multiple_databases
                        else self.conn.list_schemas()
                    )
                    adj_schemas = list(schema_set - set(self.excluded_schemas))
                else:
                    adj_schemas = [schema]
                for sch in adj_schemas:
                    if table == "*":
                        table_set = set(
                            self.conn.list_tables(database=db, schema=sch)
                            if self.allows_multiple_databases
                            else self.conn.list_tables(schema=sch)
                        )
                        adj_tables = list(table_set)
                    else:
                        adj_tables = [table]

                    for tbl in adj_tables:
                        preprocess.append((db, sch, tbl))
        msg = (
            "generating source schemas... "
            if len(preprocess) > 1
            else "generating source schema... "
        )
        for pre in tqdm(preprocess, msg):
            db, sch, tbl = pre
            location = f"{db}.{sch}"
            if with_schema:
                if self.allows_multiple_databases:
                    ibis_table = self.conn.table(database=db, schema=sch, name=tbl)
                else:
                    ibis_table = self.conn.table(schema=sch, name=tbl)
                schema = ibis_table.schema()
            sources.append(
                Source(
                    name=tbl,
                    location=location,
                    schema=(ibis_table.schema() if with_schema else None),
                )
            )

        return sources

    @classmethod
    def create_twin_connection(cls, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return ibis.duckdb.connect(path)

    def get_table(self, database, schema, table):
        conn = self.connect()
        return conn.table(database=database, schema=schema, name=table)

    def generate_twin(self, twin_path, database, schema, table, sample_row_count=1000):
        tbl = self.get_table(database, schema, table)
        row_count = tbl.count()
        # using safer random() sample
        sampled = tbl.filter(
            ibis.random() < ibis.least(sample_row_count / row_count, 1)
        )
        pyarrow_table = sampled.to_pyarrow()
        conn = self.create_twin_connection(twin_path)
        # using raw sql to set the schema since the argument is not supported in the ibis api

        # create final table
        conn.raw_sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        conn.raw_sql(f"USE {schema}")
        table_temp_name = f"table_{secrets.token_hex(8)}"
        temp_table = conn.create_table(
            table_temp_name, obj=pyarrow_table, overwrite=True
        )

        # reconnect to catch type errors
        reconn = ibis.duckdb.connect(twin_path)
        temp_table = reconn.table(table_temp_name, schema=schema)
        original_types = sampled.schema().types
        cast_dict = {}
        for i, (name, type) in enumerate(temp_table.schema().items()):
            cast_dict[name] = original_types[i]
        temp_table = temp_table.cast(cast_dict)

        # create final table and delete temp one
        final_table = conn.create_table(table, obj=temp_table, overwrite=True)
        conn.drop_table(table_temp_name)
        return final_table


class _FileConnector(_ResourceConnector):
    conn = ibis.duckdb.connect()
    paths_visited: list[str] = []
    excluded_dbs = ["system", "temp"]
    excluded_schemas = ["information_schema", "pg_catalog"]
    remote: bool

    def __init__(self, path: str):
        if scheme := extract_uri_scheme(path):
            import fsspec

            print(f"connecting to {scheme}...")
            self.conn.register_filesystem(fsspec.filesystem(scheme))
            self.remote = True
            self.path = path
        else:
            self.remote = False
            # adjust local path so it works even if you are not in the root directory
            self.path = os.path.join(get_project_directory(), path)


class DatabaseFileConnector(_FileConnector, _DatabaseConnector):
    def __init__(self, path: str, tables: list[str] = ["*.*.*"]):
        super().__init__(
            path
        )  # init method from _FileConnector, not Database Connector (because of ordering)
        self.tables = tables
        if any([len(t.split(".")) != 3 for t in tables]):
            raise ValueError(
                "tables must be a string of format 'database.schema.table'"
            )

    def list_sources(self, with_schema=False) -> list[Source]:
        out = self.find_sources_in_db(with_schema=with_schema)
        return out

    def connect(self):
        return self._connect_helper(self.conn, self.path)

    @classmethod
    @lru_cache()
    def _connect_helper(cls, conn, path):
        # caching ensures we don't attach a database from the same path twice
        if path.endswith(".duckdb"):
            name = cls.get_db_name(path)
            conn.attach(path, name)

        else:
            raise NotImplementedError(
                f"Connection for {path} not supported. Only .duckdb files are supported"
            )
        return conn

    @property
    def database(self):
        return self.get_db_name(self.path)

    @classmethod
    @lru_cache()
    def get_db_name(cls, path):
        name = Path(path).stem
        # handle situation where two database files have the same stem name
        if name in cls.conn.list_databases():
            name += str(secrets.token_hex(8))
        return name


class FileConnector(_FileConnector, _TableConnector):
    def __init__(self, path: str):
        super().__init__(
            path
        )  # init method from _FileConnector, not Database Connector (because of ordering)
        self.tbls: dict[str, ir.Table] = {}

    def connect(self):
        # caching ensures we don't attach a database from the same path twice
        self.tbls = self._connect_helper(self.conn, self.path)
        return self.conn

    def list_sources(self, with_schema=False):
        self.connect()
        return [
            Source(
                name=tbl.get_name(),
                location=path,
                schema=tbl.schema() if with_schema else None,
            )
            for path, tbl in self.tbls.items()
        ]

    @classmethod
    @lru_cache()
    def _connect_helper(cls, conn, path):
        if os.path.isdir(path):
            print(f"connecting to directory at path {path}...")
        else:
            print(f"connecting to file at path {path}...")
        stem = Path(path).stem
        tbls = {}
        # caching ensures we don't attach a database from the same path twice
        if path.endswith(".csv"):
            tbls[path] = conn.read_csv(path, table_name=stem)
        elif path.endswith(".parquet"):
            tbls[path] = conn.read_parquet(path, table_name=stem)
        elif path.endswith(".json"):
            tbls[path] = conn.read_json(path, table_name=stem)
        elif os.path.isdir(path):
            for sub in os.listdir(path):
                path_it = os.path.join(path, sub)
                # only looking at files prevents recursion into subdirectories
                if os.path.isfile(path_it) and not sub.startswith("."):
                    tbls.update(cls._connect_helper(conn, path_it))

        else:
            raise NotImplementedError(
                f"Connection for {path} not supported. Only .csv, .parquet, and .json files are supported"
            )

        return tbls


class BigQueryConnector(_DatabaseConnector):
    def __init__(
        self,
        tables: list[str],
        service_account_path: str | None = None,
        service_account_info: str | None = None,
    ):
        from google.oauth2 import service_account

        if service_account_path is not None:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
        elif service_account_info is not None:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(service_account_info)
            )
        else:
            credentials = None

        self.credentials = credentials
        self.tables = tables

    def connect(self):
        self.conn = BigQueryConnector._connect_helper(self.credentials)
        return self.conn

    def list_sources(self, with_schema=False) -> list[Source]:
        self.connect()
        return self.find_sources_in_db(with_schema=with_schema)

    # caching ensures we create one bq connection per set of credentials across instances of the class
    @staticmethod
    @lru_cache()
    def _connect_helper(credentials):
        print("connecting to bigquery...")
        return ibis.bigquery.connect(credentials=credentials)


class PostgresConnector(_DatabaseConnector):
    excluded_schemas = [
        "information_schema",
        "pg_catalog",
        "pgsodium",
        "auth",
        "extensions",
        "net",
    ]
    allows_multiple_databases: bool = False

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        tables: list[str],
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.tables = tables

        # postgres requires connecting at the database level
        dbs = set([t.split(".")[0] for t in tables])
        if len(dbs) > 1 or "*" in dbs:
            raise ValueError("Postgres connector only supports one database at a time")
        self.database = dbs.pop()

    def connect(self):
        self.conn = self._connect_helper(
            self.host, self.port, self.user, self.password, self.database
        )
        return self.conn

    def list_sources(self, with_schema=False) -> list[Source]:
        self.connect()
        return self.find_sources_in_db(with_schema=with_schema)

    # caching ensures we create one bq connection per set of credentials across instances of the class
    @staticmethod
    @lru_cache()
    def _connect_helper(host: str, port: int, user: str, password: str, database: str):
        print(f"connecting to postgres {host}...")
        return ibis.postgres.connect(
            host=host, port=port, user=user, password=password, database=database
        )
